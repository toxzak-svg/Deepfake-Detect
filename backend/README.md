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

To enable the baseline model demo (frame-level inference) install the ML requirements:

```bash
pip install -r requirements-ml.txt
```

The `/detect` endpoint will attempt to run the baseline detector for simple image URLs (jpg/png). This is a demo scaffold — for production install GPU drivers and serve with Triton or a model server.
