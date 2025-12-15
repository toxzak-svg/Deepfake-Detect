from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

# Add backend root to path so we can import models from backend/models
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from models.baseline import BaselineDetector
from config import ALLOWED_API_KEYS, RATE_LIMIT_PER_MIN
import httpx
import numpy as np
import cv2
import csv
from pathlib import Path
import asyncio
import tempfile
import subprocess
import glob
import os


app = FastAPI(title="Deepfake-Detect Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DetectRequest(BaseModel):
    url: str
    source: str | None = None


class DetectResponse(BaseModel):
    score: float
    flags: list[str]
    details: dict | None = None


detector = BaselineDetector()

# Simple in-memory rate limiter: fixed window per API key
_rate_windows: dict[str, dict] = {}


def _check_rate_limit(key: str) -> tuple[bool, int]:
    """Return (allowed, remaining) for the fixed 60s window."""
    import time

    limit = RATE_LIMIT_PER_MIN
    window = 60
    now = int(time.time())
    w_start = now - (now % window)
    info = _rate_windows.get(key)
    if not info or info.get("start") != w_start:
        _rate_windows[key] = {"start": w_start, "count": 0}
        info = _rate_windows[key]
    if info["count"] >= limit:
        return False, 0
    info["count"] += 1
    remaining = max(0, limit - info["count"])
    return True, remaining


def _get_key_from_header(headers) -> str | None:
    # FastAPI request.headers behaves like a dict
    return headers.get("x-api-key") or headers.get("X-Api-Key")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/detect", response_model=DetectResponse)
async def detect(req: DetectRequest):
    """Detection endpoint — lightweight demo pipeline.

    - If `url` looks like an image, fetch and run the baseline frame detector.
    - Otherwise apply fast heuristics on the URL text.
    """
    if not req.url:
        raise HTTPException(status_code=400, detail="url required")

    # Auth: require API key for detection endpoints
    from fastapi import Request
    # extract headers via request state if available (FastAPI passes header via dependency normally)
    # In this handler we can access the current request using inspect of context; simpler: use Starlette's request in app state
    # But the Next.js proxy will include the header; FastAPI exposes headers via `Request` dependency if needed.
    # We'll check environ variable fallback for internal calls if header missing.
    try:
        from fastapi import Request
        # if running in ASGI context, get header from Request via dependency injection is better
    except Exception:
        pass

    # Check header in ASGI scope
    try:
        # Retrieve header from FastAPI's request via starlette 'request' in scope
        import inspect
        frame = inspect.currentframe()
        # walk back to find 'request' in locals (best-effort)
        req_obj = None
        f = frame
        while f:
            if 'request' in f.f_locals:
                req_obj = f.f_locals['request']
                break
            f = f.f_back
        header_key = None
        if req_obj is not None:
            header_key = _get_key_from_header(req_obj.headers)
    except Exception:
        header_key = None

    if not header_key:
        # fallback to environment or default demo key
        header_key = None
    if header_key not in ALLOWED_API_KEYS:
        raise HTTPException(status_code=401, detail="invalid or missing API key")

    allowed, remaining = _check_rate_limit(header_key)
    if not allowed:
        raise HTTPException(status_code=429, detail="rate limit exceeded")

    url_lower = req.url.lower()
    score = 0.05
    flags: list[str] = []

    # Fast heuristic checks
    if "giveaway" in url_lower or "airdrop" in url_lower:
        score = 0.7
        flags.append("contains_giveaway_keyword")

    # If URL points to an image, attempt to fetch and run baseline model
    if any(req.url.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".webp")):
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                r = await client.get(req.url)
                r.raise_for_status()
                data = np.frombuffer(r.content, dtype=np.uint8)
                img = cv2.imdecode(data, cv2.IMREAD_COLOR)
                if img is None:
                    raise ValueError("could not decode image")
                # convert BGR -> RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                probs = detector.predict_frames([img])
                img_score = float(np.mean(probs))
                # blend heuristic and model score
                score = max(score, img_score * 0.95)
                if img_score > 0.6:
                    flags.append("model_suspect_frame")
        except Exception as e:
            # non-fatal: return heuristic result and note the error
            return {"score": score, "flags": flags, "details": {"source": req.source, "error": str(e)}}

    # If URL looks like a video (YouTube) try to download and extract frames
    if any(x in url_lower for x in ("youtube.com", "youtu.be")) or ".mp4" in url_lower:
        try:
            async def run_extract_and_score(url: str) -> float | None:
                with tempfile.TemporaryDirectory() as tmpdir:
                    out_dir = Path(tmpdir) / "frames"
                    cmd = [sys.executable, str(ROOT / "scripts" / "extract_frames.py"), url, str(out_dir), "4"]

                    def run_cmd():
                        subprocess.check_call(cmd)

                    await asyncio.to_thread(run_cmd)

                    frames = []
                    for p in sorted(out_dir.glob("*.jpg")):
                        im = cv2.imread(str(p))
                        if im is None:
                            continue
                        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                        frames.append(im)
                    if not frames:
                        return None
                    probs = detector.predict_frames(frames)
                    return float(np.mean(probs))

            vid_score = await run_extract_and_score(req.url)
            if vid_score is not None:
                score = max(score, vid_score * 0.95)
                if vid_score > 0.6:
                    flags.append("model_suspect_video_frames")
        except Exception as e:
            # non-fatal; return heuristic result with error
            return {"score": score, "flags": flags, "details": {"source": req.source, "error": str(e)}}

    return {"score": score, "flags": flags, "details": {"source": req.source}}


LABELS_FILE = ROOT / "data" / "labels.csv"
SEED_FILE = ROOT / "data" / "seed_urls.txt"
LABELS_FILE.parent.mkdir(parents=True, exist_ok=True)


@app.get("/seed")
async def seed_urls():
    """Return seed URLs for labeling (reads backend/data/seed_urls.txt)."""
    if not SEED_FILE.exists():
        return {"urls": []}
    with SEED_FILE.open("r", encoding="utf-8") as f:
        urls = [l.strip() for l in f.readlines() if l.strip()]
    return {"urls": urls}


class LabelRequest(BaseModel):
    url: str
    label: str
    reporter: str | None = None


@app.post("/label")
async def label(req: LabelRequest):
    """Append a label to the labels CSV file."""
    LABELS_FILE.parent.mkdir(parents=True, exist_ok=True)
    created = not LABELS_FILE.exists()
    with LABELS_FILE.open("a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if created:
            writer.writerow(["url", "label", "reporter"])
        writer.writerow([req.url, req.label, req.reporter or "anonymous"])
    return {"ok": True}
