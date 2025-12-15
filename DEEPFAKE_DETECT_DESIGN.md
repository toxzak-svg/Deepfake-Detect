# Deepfake-Detect — Design & Research

## Goal

Build an accurate, scalable system that detects and flags deepfake-driven crypto airdrops and giveaway scams across video, audio, text, social platforms, and on-chain activity while minimizing false positives and legal risk.

## Key detection signals (multimodal)
- **Video/Image Deepfake:** frame artifacts, temporal inconsistency, lighting/texture anomalies, encoder fingerprints.
- **Audio Deepfake:** mel-spectrogram anomalies, speaker-embedding mismatches, lip-sync inconsistency.
- **Text / NLP:** giveaway templates, urgency cues, impersonation language, claims of token rewards.
- **Account & Social Signals:** account age, follower growth velocity, repost networks, bot-likeness scores.
- **On-chain Signals:** new token contracts, low liquidity, token distribution patterns, approval/transfer anomalies.
- **Metadata & Provenance:** upload history, EXIF/metadata mismatch, re-encoding traces.
- **URL / Domain Signals:** newly-registered domains, homograph/phishing checks, TLS anomalies.

## Recommended MVP architecture
- **Ingest:** connectors for major social platforms (X/Meta/YouTube), Telegram/Discord scrapers (respecting terms), blockchain node/webhooks.
- **Preprocess:** extract frames, audio tracks, text (captions, descriptions), and metadata; canonicalize timestamps.
- **Model layer:**
  - Frame + temporal video deepfake detector (CNN + temporal module).
  - Audio deepfake detector (spectrogram & speaker-embedding checks).
  - NLP classifier for text and metadata.
  - Social graph / account fraud detector.
  - On-chain heuristic engine for token and airdrop anomalies.
- **Ensemble & Rules:** weighted scoring with deterministic overrides for high-confidence blocklist matches.
- **Storage & infra:** S3-compatible object store, Postgres for metadata, Redis for queues, Kafka for streams. Model serving via Triton or TorchServe, API via FastAPI, frontend via Next.js.
- **UX:** evidence timeline, manual review queue, reporter reputation, appeal flow.

## Innovative differentiators
- **Wallet-integrated warnings:** browser/extension checks that warn users before token approvals or airdrop interactions.
- **Chain-aware provenance:** correlate media claims with on-chain events to validate legitimacy of airdrops.
- **Tamper-evident evidence bundles:** cryptographically-signed snapshots for takedowns or legal requests.
- **On-device lightweight detectors:** privacy-preserving checks in browser extensions for fast feedback.
- **Federated/adaptive learning:** share model improvements with partners without sharing PII.
- **Automated adversarial augmentation:** synthesize controlled deepfakes to strengthen training data and improve robustness.

## MVP roadmap (short)
1. Collect seed dataset: public scam examples, manual labels, and synthetic deepfakes.  
2. Implement baseline detectors: image/video classifier, simple NLP heuristics, and on-chain rules.  
3. Build ingestion pipeline + minimal Next.js dashboard + reporting API.  
4. Add browser extension for in-page flags and wallet warnings.  
5. Pilot with community/exchange; gather labels and iterate.

## Metrics & success criteria
- Precision at operational threshold (prioritize precision to reduce false takedowns).
- Recall for high-risk items.
- False positive rate acceptable to partners.
- Time-to-detect for high-risk items (seconds–minutes target).
- Manual review workload and analyst throughput.

## Major risks & mitigations
- **False positives / legal takedowns:** show clear evidence, provide appeals, engage legal counsel.  
- **TOS/privacy violations while scraping:** prefer official APIs and partner integrations; minimize PII and store only what's needed.  
- **Adversarial evasion and poisoning:** adversarial training, anomaly detectors, red-team testing.  
- **Label scarcity:** use synthetic generation, active learning, and paid labeling.  
- **Cost & scale:** fast heuristics first, heavy inference only on high-scoring items; use edge inference where possible.

## Suggested tech stack
- Frontend: Next.js (existing).  
- API & orchestration: FastAPI (Python).  
- Models: PyTorch; serve via NVIDIA Triton or TorchServe.  
- Streaming: Kafka or Kinesis.  
- Storage: S3, Postgres, Redis.  
- Infra: Docker + Kubernetes, CI/CD via GitHub Actions.  
- Observability: Prometheus + Grafana, Sentry for errors.

## Next steps (concrete)
1. Finalize scope & threat model and get legal sign-off for data collection.  
2. Start seed dataset collection and annotation plan.  
3. Prototype baseline image/video detector and a minimal ingestion pipeline.  
4. Add reporting API and a minimal Next.js UI to display flagged items and evidence.  

---
