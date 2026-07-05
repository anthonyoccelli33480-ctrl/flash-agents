<div align="center">

# ⚡ Flash Agents

**40 one-shot AI agents on [Cerebras Inference](https://inference-docs.cerebras.ai) — sub-second tasks, zero chat overhead.**

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agents](https://img.shields.io/badge/agents-40-amber.svg)](#-agent-catalog)
[![Python](https://img.shields.io/badge/python-3.12+-3776AB?logo=python&logoColor=white)](backend/)
[![React](https://img.shields.io/badge/react-19-61DAFB?logo=react&logoColor=black)](frontend/)
[![Cerebras](https://img.shields.io/badge/inference-Cerebras-ff6b00)](https://cloud.cerebras.ai)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](backend/app/main.py)

*Paste → Run → Structured JSON in ~300–800ms. No chains. No memory. No 429 spam.*

[Quick Start](#-quick-start) · [Agents](#-agent-catalog) · [Architecture](#-architecture) · [Why Flash Agents?](#-why-flash-agents)

</div>

---

## 🎯 What is this?

**Flash Agents** is an open-source showcase for **ultra-fast LLM inference** on Cerebras. Each agent does **exactly one job** with the **best model** for that job:

| Model | Use case | Agents |
|-------|----------|--------|
| **GLM 4.7** (`zai-glm-4.7`) | Code, debug, regex, secrets | 13 |
| **GPT OSS 120B** (`gpt-oss-120b`) | Reasoning, product, career, security | 20 |
| **Gemma 4 31B** (`gemma-4-31b`) | Vision — screenshots, OCR, UI audit | 7 |

Built for developers who want **ChatGPT-speed UX** without building a chatbot.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│ React UI    │────▶│ FastAPI proxy│────▶│ Cerebras API    │
│ onboarding  │     │ rate-gate    │     │ GLM · 120B ·    │
│ image upload│     │ JSON schema  │     │ Gemma vision    │
└─────────────┘     └──────────────┘     └─────────────────┘
```

## ✨ Highlights

- ⚡ **One task = one API call** — no multi-turn chat, no agent loops
- 📊 **Structured JSON output** — `response_format: json_object`, ready to pipe into tools
- 🖼️ **Vision agents** — upload PNG/JPEG, get UX audits, OCR, diagram explanations
- 🛡️ **Rate-safe** — built-in 15s gate for Cerebras free tier (~5 req/min)
- 🔐 **Local secrets** — API key in `.env` on your machine, never sent to the browser
- 🧭 **Onboarding built-in** — explains the app + validates your Cerebras key on first run
- 🍎 **macOS launcher** — double-click `.command` on Desktop to start everything

## 🚀 Quick Start

### 1. Get a free Cerebras API key

→ [cloud.cerebras.ai](https://cloud.cerebras.ai) (models: `zai-glm-4.7`, `gpt-oss-120b`, `gemma-4-31b`)

### 2. Install & run

```bash
git clone https://github.com/YOUR_USERNAME/flash-agents.git
cd flash-agents
cp .env.example .env   # add CEREBRAS_API_KEY=csk-...

make install           # Python 3.12 venv + npm
make backend           # http://127.0.0.1:8787
make frontend          # http://127.0.0.1:5173
```

Or on macOS: double-click **`⚡ Lancer Flash Agents.command`** from the Desktop folder.

### 3. Try an agent

| Try this | Input | Output |
|----------|-------|--------|
| **Flash Review** | Paste a code diff | Score, critical issues, verdict |
| **Flash Fix** | Stack trace + code | Root cause + patch |
| **Flash UI Review** | Screenshot PNG | UX critique JSON |
| **Flash MVP** | Vague startup idea | Scoped MVP plan |

## 🤖 Agent Catalog

<details>
<summary><strong>Dev (11)</strong> — GLM 4.7</summary>

| Agent | One-liner |
|-------|-----------|
| Flash Review | Code review → structured score + fixes |
| Flash Fix | Stack trace → root cause + patch |
| Flash Commit | Git diff → Conventional Commits + PR |
| Flash Regex | Natural language → tested regex |
| Flash Test | Function → unit tests |
| Flash SQL | Question + schema → SQL query |
| Flash Explain | Code → clear explanation |
| Flash Refactor | Code smell → clean version |
| Flash Docker | Stack → minimal Dockerfile |
| Flash OpenAPI | Endpoints → OpenAPI spec |
| Flash Migrate | Framework A → migration plan B |

</details>

<details>
<summary><strong>Career (5)</strong> — 120B + README on GLM</summary>

Flash JD · Flash STAR · Flash LinkedIn · Flash Email · Flash README

</details>

<details>
<summary><strong>Product (6)</strong> — GPT OSS 120B</summary>

Flash MVP · Flash Decision · Flash Pitch · Flash Competitor · Flash Pricing · Flash Onboarding

</details>

<details>
<summary><strong>AI / ML (5)</strong> — 120B + Router on GLM</summary>

Flash Eval · Flash Prompt · Flash Dataset · Flash Rubric · Flash Router

</details>

<details>
<summary><strong>Content (3)</strong> — GPT OSS 120B</summary>

Flash TL;DR · Flash Compare · Flash Outline

</details>

<details>
<summary><strong>Security (3)</strong> — 120B + Secret on GLM</summary>

Flash Threat · Flash Secret · Flash RGPD

</details>

<details>
<summary><strong>Vision (7)</strong> — Gemma 4 31B + image upload</summary>

Flash UI Review · Flash Diagram · Flash Wireframe · Flash OCR · Flash A11y · Flash Chart · Flash Mockup

</details>

Full reference → [docs/AGENTS.md](docs/AGENTS.md)

## 🆚 Why Flash Agents?

| | Flash Agents | Typical agent framework |
|--|--------------|-------------------------|
| Latency | **~300–800ms** visible | Hidden in multi-step chains |
| Calls per task | **1** | 5–50+ tool loops |
| Output | **JSON schema** | Free-form markdown |
| Infra | FastAPI + React | LangChain, vector DB, memory |
| Best for | **Single-shot tasks** | Long-running autonomous agents |

> Not a replacement for Jarvis, AutoGPT, or CrewAI — a **complement** for when you want speed and structure.

## 🏗 Architecture

- **Frontend** — React 19 + Vite, onboarding flow, image upload for vision agents
- **Backend** — FastAPI proxy, Cerebras OpenAI-compatible client, retry on `queue_exceeded`
- **Rate gate** — configurable interval (`FLASH_RATE_INTERVAL_SEC`, default 15s)
- **Guides** — each agent returns `how_to` + `next_steps` after every run

## ➕ Add an agent

Edit `backend/app/agents/registry.py`:

```python
_register(AgentDef(
    id="my_agent",
    name="Flash My Agent",
    tagline="Input → output in one shot",
    model="zai-glm-4.7",  # or gpt-oss-120b, gemma-4-31b
    category="dev",
    icon="⚡",
    placeholder="Paste your input…",
    system="""Respond ONLY in JSON: { "result": "..." }""",
))
```

## 🔑 Keywords

`cerebras` · `llm-agents` · `ai-agents` · `inference` · `fastapi` · `react` · `vision-llm` · `gemma` · `glm-4` · `code-review` · `developer-tools` · `one-shot-agents` · `structured-output` · `open-source`

## 📜 License

MIT — see [LICENSE](LICENSE)

---

<div align="center">

**If Flash Agents saved you time, a ⭐ helps others find it.**

Built to show what [Cerebras Inference](https://inference-docs.cerebras.ai) feels like when you don't slow it down.

</div>