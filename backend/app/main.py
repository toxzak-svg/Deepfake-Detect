from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

# Add backend root to path so we can import models from backend/models
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from models.baseline import BaselineDetector
import httpx
import numpy as np
import cv2
import csv
from pathlib import Path


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


detector = BaselineDetector(device="cpu")


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
