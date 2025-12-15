# Backend (FastAPI)

Quick start (requires Python 3.10+):

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\Activate on Windows
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:
- `GET /health` — health check
- `POST /detect` — accepts JSON `{ "url": "...", "source": "..." }` and returns a stubbed detection result

Replace the stub with a real ingestion and inference pipeline as you progress.

Model demo
----------


Authentication & Rate Limiting
------------------------------

This prototype enforces a simple API key check on the `/detect` and `/label` endpoints. Keys are read from the `DEEPFAKE_API_KEYS` environment variable (comma-separated). If not set, a default `demo-key` is accepted.

Example (Linux/macOS):

```bash
export DEEPFAKE_API_KEYS=demo-key,my-production-key
export DEEPFAKE_RATE_LIMIT_PER_MIN=120
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Requests must include header `x-api-key: <key>`. The backend enforces a fixed-window rate limit per key based on `DEEPFAKE_RATE_LIMIT_PER_MIN`.

This is a prototype-only approach — for production use a persistent rate limiter (Redis), robust auth (JWT/OAuth2), and proper key management.
To enable the baseline model demo (frame-level inference) install the ML requirements:

```bash
pip install -r requirements-ml.txt
```

The `/detect` endpoint will attempt to run the baseline detector for simple image URLs (jpg/png). This is a demo scaffold — for production install GPU drivers and serve with Triton or a model server.
