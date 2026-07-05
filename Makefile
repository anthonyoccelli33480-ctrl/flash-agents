.PHONY: dev backend frontend install

install:
	cd backend && uv venv --python 3.12 .venv && uv pip install -r requirements.txt --python .venv/bin/python
	cd frontend && npm install

backend:
	cd backend && .venv/bin/uvicorn app.main:app --reload --port 8787

frontend:
	cd frontend && npm run dev

dev:
	@echo "Lance backend et frontend dans deux terminaux : make backend && make frontend"