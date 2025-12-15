"""Configuration helpers for backend.

Reads `DEEPFAKE_API_KEYS` from environment (comma-separated). Falls back to a demo key.
"""
import os


def get_api_keys():
    raw = os.environ.get("DEEPFAKE_API_KEYS")
    if raw:
        return [k.strip() for k in raw.split(",") if k.strip()]
    # default demo key (do NOT use in production)
    return ["demo-key"]


ALLOWED_API_KEYS = get_api_keys()


RATE_LIMIT_PER_MIN = int(os.environ.get("DEEPFAKE_RATE_LIMIT_PER_MIN", "60"))
