# Changelog

## [1.0.0] — 2026-07-06

### Added

- 40 one-shot agents across dev, career, product, AI, content, security, vision
- React 19 UI with category sidebar, latency display, guide panel
- Onboarding flow with Cerebras API key validation + `.env` storage
- 7 vision agents (Gemma 4 31B) with image upload
- Rate gate (15s) for Cerebras free tier
- macOS Desktop launcher (`.command` scripts)
- FastAPI proxy — API key never exposed to browser

### Models

- `zai-glm-4.7` — coding & tool-use
- `gpt-oss-120b` — reasoning & planning
- `gemma-4-31b` — vision tasks