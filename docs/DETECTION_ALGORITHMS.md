# Detection Algorithms Design

Multimodal detectors:
- Video deepfake: frame-level CNN + temporal modeling (I3D / Transformers over frames).
- Audio deepfake: spectrogram classifiers + speaker verification checks.
- NLP: classification on captions/descriptions and comment analysis.
- Social graph: account-age, follower-growth, repost topology, bot detection.
- On-chain heuristics: token liquidity, contract age, approval patterns.

Ensemble:
- Weighted scoring with deterministic rule overrides for blocklists and known malicious indicators.
