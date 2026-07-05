# GitHub Launch Playbook

How to make discovery bots and humans find Flash Agents.

## ⚠️ Private vs public

**Bots only scan public repos.** Private = invisible to trending crawlers, awesome-lists, and star aggregators.

Recommended flow:

1. Push **private** first → test CI green
2. Flip **public** when ready: `gh repo edit --visibility public`
3. Blast within 24h (GitHub trending favors fresh activity)

## Repo metadata (already prepared)

| Field | Value |
|-------|-------|
| **Description** | `40 one-shot AI agents on Cerebras Inference — sub-second JSON tasks, vision, rate-safe` |
| **Website** | Link to demo GIF or Cerebras docs |
| **Topics** | See `.github/TOPICS.txt` |

## What bots index

- README keywords: `cerebras`, `llm-agents`, `inference`, `fastapi`, `vision-llm`
- Green CI badge on README (add after first push)
- Recent commits + releases
- `MIT` license file
- Issue templates + CONTRIBUTING = maturity signals

## Launch checklist

- [ ] Add 10s demo GIF to README (`docs/demo.gif`)
- [ ] Replace `YOUR_USERNAME` in README clone URL
- [ ] `gh repo edit --visibility public`
- [ ] Post on X: *"40 one-shot agents on Cerebras — 300ms code review, vision OCR, no LangChain"*
- [ ] Submit to [awesome-cerebras](https://github.com/search?q=awesome+cerebras) lists if they exist
- [ ] Hacker News Show HN (Tuesday–Thursday morning US time works best)
- [ ] r/LocalLLaMA, r/MachineLearning — focus on speed + structured JSON

## Star velocity tips

- Pin the repo on your GitHub profile
- Cross-link from Jarvis OS or other projects
- Respond to issues within 24h (activity score)
- Tag `@cerebras_ai` on social — they sometimes RT showcase projects