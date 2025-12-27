from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys
import uuid

# Add backend root to path so we can import models from backend/models
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from models.baseline import BaselineDetector
from config import ALLOWED_API_KEYS, RATE_LIMIT_PER_MIN
from config import PERPLEXITY_API_KEY, PERPLEXITY_BASE_URL, PERPLEXITY_MODEL, PERPLEXITY_TIMEOUT
from app.services.perplexity import create_perplexity_service
from app.services.api_key_manager import APIKeyManager
from app.services.webhook_service import WebhookService
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
from typing import Optional


app = FastAPI(title="DeepfakeGuard API", version="1.0.0")

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

# Initialize Perplexity service if API key is available
perplexity_service = None
if PERPLEXITY_API_KEY:
    try:
        perplexity_service = create_perplexity_service(
            api_key=PERPLEXITY_API_KEY,
            base_url=PERPLEXITY_BASE_URL,
            model=PERPLEXITY_MODEL,
            timeout=PERPLEXITY_TIMEOUT
        )
    except Exception as e:
        print(f"Warning: Could not initialize Perplexity service: {e}")

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


@app.post("/v1/scan", response_model=DetectResponse)
async def scan_media(
    req: DetectRequest,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """
    Scan media for deepfake detection.
    
    This is the primary API endpoint for customers. Requires API key authentication.
    Supports images and videos via URL.
    
    **Authentication**: Include your API key in the `X-API-Key` header.
    
    **Free tier**: 10 scans/month
    **Pro tier**: 500 scans/month with manual review
    **Enterprise tier**: Unlimited scans with dedicated review team
    """
    if not req.url:
        raise HTTPException(status_code=400, detail="url is required")
    
    # Validate API key and check usage limits
    is_valid, user_data, error_msg = APIKeyManager.validate_api_key(x_api_key)
    if not is_valid:
        raise HTTPException(status_code=401, detail=error_msg or "Invalid API key")
    
    scan_id = str(uuid.uuid4())

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


@app# Record scan usage
    scan_data = {
        'url': req.url,
        'score': score,
        'flags': flags,
        'scan_id': scan_id,
    }
    scan_record = APIKeyManager.increment_usage(x_api_key, scan_data)
    
    # Send webhooks if configured
    webhook_url = user_data.get('webhook_url')
    if webhook_url:
        # Send scan completed webhook
        asyncio.create_task(WebhookService.notify_scan_completed(
            webhook_url=webhook_url,
            scan_id=scan_id,
            result=scan_data
        ))
        
        # If flagged, send additional alert
        if score > 0.6:
            asyncio.create_task(WebhookService.notify_scan_flagged(
                webhook_url=webhook_url,
                scan_id=scan_id,
                result=scan_data
            ))
    
    # Get remaining scans
    stats = APIKeyManager.get_user_stats(x_api_key)
    
    return {
        "score": score,
        "flags": flags,
        "details": {
            "source": req.source,
            "scan_id": scan_id,
            "manual_review_pending": scan_record.get('manual_review_pending', False),
            "scans_remaining": stats.get('scans_remaining'),
        }
    }


# ========== API Key & Account Management ==========


class CreateAccountRequest(BaseModel):
    email: str
    tier: str = 'free'
    webhook_url: Optional[str] = None


class UpdateWebhookRequest(BaseModel):
    webhook_url: str


@app.post("/v1/account/create")
async def create_account(req: CreateAccountRequest):
    """Create a new API account. Used by the signup flow."""
    try:
        user_data = APIKeyManager.create_user(
            email=req.email,
            tier=req.tier,
            webhook_url=req.webhook_url
        )
        return {
            "success": True,
            "api_key": user_data['api_key'],
            "email": user_data['email'],
            "tier": user_data['tier'],
            "scans_limit": APIKeyManager.TIERS[user_data['tier']]['scans_per_month'],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/v1/account/stats")
async def get_account_stats(x_api_key: Optional[str] = Header(None, alias="X-API-Key")):
    """Get usage statistics for your account."""
    is_valid, user_data, error_msg = APIKeyManager.validate_api_key(x_api_key)
    if not is_valid:
        raise HTTPException(status_code=401, detail=error_msg or "Invalid API key")
    
    stats = APIKeyManager.get_user_stats(x_api_key)
    return stats


@app.post("/v1/account/webhook")
async def update_webhook(
    req: UpdateWebhookRequest,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Update webhook URL for scan notifications."""
    is_valid, user_data, error_msg = APIKeyManager.validate_api_key(x_api_key)
    if not is_valid:
        raise HTTPException(status_code=401, detail=error_msg or "Invalid API key")
    
    success = APIKeyManager.update_webhook_url(x_api_key, req.webhook_url)
    if success:
        return {"success": True, "webhook_url": req.webhook_url}
    else:
        raise HTTPException(status_code=500, detail="Failed to update webhook")


# ========== Admin Endpoints (Manual Review) ==========


class ReviewDecisionRequest(BaseModel):
    scan_id: str
    verdict: str  # 'confirmed', 'false_positive', 'uncertain'
    notes: Optional[str] = None


@app.get("/admin/pending-reviews")
async def get_pending_reviews(admin_key: Optional[str] = Header(None, alias="X-Admin-Key")):
    """Get all scans pending manual review (admin only)."""
    # Simple admin auth - in production use proper auth
    if admin_key != "admin_secret_key_change_me":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    pending = APIKeyManager.get_pending_reviews()
    return {"pending_reviews": pending, "count": len(pending)}


@app.post("/admin/review-decision")
async def submit_review_decision(
    req: ReviewDecisionRequest,
    admin_key: Optional[str] = Header(None, alias="X-Admin-Key")
):
    """Submit manual review decision (admin only)."""
    if admin_key != "admin_secret_key_change_me":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # TODO: Update scan record with review decision
    # TODO: Send webhook notification to customer
    
    return {
        "success": True,
        "scan_id": req.scan_id,
        "verdict": req.verdict,
    }


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

    

# ========== Perplexity AI Endpoints ==========


class PerplexityAnalysisRequest(BaseModel):
    url: str
    description: str | None = None
    additional_context: str | None = None


class PerplexityWalletRequest(BaseModel):
    address: str


class PerplexityEndorsementRequest(BaseModel):
    celebrity_name: str
    crypto_project: str
    claim: str | None = None


class PerplexityTextRequest(BaseModel):
    text: str


@app.post("/perplexity/analyze-scam")
async def analyze_scam_with_perplexity(req: PerplexityAnalysisRequest):
    """Analyze a URL for scam indicators using Perplexity AI's real-time web search.

    This endpoint provides enhanced threat intelligence by searching the web
    for known scam reports, domain history, and similar fraud patterns.
    """
    if not perplexity_service:
        raise HTTPException(
            status_code=503,
            detail="Perplexity service not configured. Set PERPLEXITY_API_KEY environment variable."
        )

    result = await perplexity_service.analyze_scam_indicators(
        url=req.url,
        description=req.description,
        additional_context=req.additional_context
    )

    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Analysis failed"))

    return result


@app.post("/perplexity/research-wallet")
async def research_wallet_with_perplexity(req: PerplexityWalletRequest):
    """Research a cryptocurrency wallet address for scam history using Perplexity AI.

    This endpoint searches for known scam reports, transaction patterns,
    and reputation information about a wallet address.
    """
    if not perplexity_service:
        raise HTTPException(
            status_code=503,
            detail="Perplexity service not configured. Set PERPLEXITY_API_KEY environment variable."
        )

    result = await perplexity_service.research_wallet_address(address=req.address)

    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Research failed"))

    return result


@app.post("/perplexity/verify-endorsement")
async def verify_endorsement_with_perplexity(req: PerplexityEndorsementRequest):
    """Verify celebrity endorsement claims using Perplexity AI.

    This endpoint fact-checks claims about celebrity crypto endorsements
    by searching for official statements and news from reputable sources.
    """
    if not perplexity_service:
        raise HTTPException(
            status_code=503,
            detail="Perplexity service not configured. Set PERPLEXITY_API_KEY environment variable."
        )

    result = await perplexity_service.verify_celebrity_endorsement(
        celebrity_name=req.celebrity_name,
        crypto_project=req.crypto_project,
        claim=req.claim
    )

    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Verification failed"))

    return result


@app.post("/perplexity/analyze-text")
async def analyze_text_with_perplexity(req: PerplexityTextRequest):
    """Analyze text content for scam patterns using Perplexity AI.

    This endpoint identifies urgency tactics, promises of guaranteed returns,
    impersonation language, and other common scam indicators in text.
    """
    if not perplexity_service:
        raise HTTPException(
            status_code=503,
            detail="Perplexity service not configured. Set PERPLEXITY_API_KEY environment variable."
        )

    result = await perplexity_service.analyze_text_for_scam_patterns(text=req.text)

    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Analysis failed"))

    return result

