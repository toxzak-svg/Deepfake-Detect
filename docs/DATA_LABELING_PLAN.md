# Data Sources & Labeling Plan

Sources:
- Public posts from YouTube, X, Instagram (via APIs where available).
- Telegram / Discord channel captures (with operator consent or public channels).
- Blockchain explorers and token metadata feeds.

Labeling strategy:
- Seed with public scam examples, augmented with synthetic deepfakes.
- Use a mix of expert labeling and paid crowd labels for scale.
- Capture metadata and provenance with each label (uploader, timestamp, URL, contract address).

Storage and privacy:
- Store minimal PII, keep raw media in S3-like storage with restricted access.
