# Deployment, Scaling & Resiliency

Recommendations:
- Use K8s for autoscaling model servers and FastAPI workers.
- Triage pipeline: fast heuristics at edge, heavy inference for high-scoring items.
- Caching for repeated URLs and rate-limiting for public API.
- Use CDN and DDoS protection for frontend endpoints.
