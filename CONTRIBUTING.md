# Contributing

Thanks for helping make Flash Agents easier to discover and use.

## Add an agent

1. Register in `backend/app/agents/registry.py`
2. Add guide strings in `backend/app/agents/guides.py`
3. Pick the right model:
   - **GLM 4.7** — code, regex, secrets, routing
   - **GPT OSS 120B** — reasoning, writing, product
   - **Gemma 4 31B** — vision (set `requires_image=True`)
4. System prompt must request **JSON-only** output
5. Open a PR — CI checks agent count + frontend build

## Run locally

```bash
make install && make backend && make frontend
```

## Code style

- Match existing patterns in `registry.py` and React components
- No API keys in code or commits
- French OK in agent prompts; README/docs in English for reach