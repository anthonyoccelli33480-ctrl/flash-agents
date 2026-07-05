# Security

## API keys

- Store `CEREBRAS_API_KEY` in `.env` at repo root (gitignored, chmod 600)
- Never commit `.env` or paste keys in issues/PRs
- The browser never receives your key after onboarding — FastAPI proxies all calls

## Reporting vulnerabilities

Open a private security advisory on GitHub or email the maintainer. Do not disclose API keys in public issues.