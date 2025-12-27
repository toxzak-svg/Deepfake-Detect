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


# Perplexity AI configuration
PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY")
PERPLEXITY_BASE_URL = "https://api.perplexity.ai"
PERPLEXITY_MODEL = os.environ.get("PERPLEXITY_MODEL", "llama-3.1-sonar-small-128k-online")
PERPLEXITY_TIMEOUT = int(os.environ.get("PERPLEXITY_TIMEOUT", "30"))
