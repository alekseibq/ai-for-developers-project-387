POETRY = $(shell command -v poetry 2>/dev/null || echo ~/.local/bin/poetry)

.PHONY: dev dev-rebuild dev-backend dev-frontend build test lint coverage generate e2e e2e-dev ci docker-clean

dev:
	docker compose up --build

dev-rebuild:
	docker compose down --remove-orphans && docker compose up --build -d

dev-backend:
	cd backend && $(POETRY) run uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

generate:
	cd typespec && npm run compile

test:
	cd backend && $(POETRY) run pytest -v

coverage:
	cd backend && $(POETRY) run coverage run -m pytest -v && $(POETRY) run coverage report -m

lint:
	cd backend && $(POETRY) run ruff check .
	cd backend && $(POETRY) run mypy app/
	cd backend && $(POETRY) run bandit -r app/ -c .bandit
	cd frontend && npm run lint

e2e:
	docker compose --profile e2e up --build --abort-on-container-exit e2e

e2e-dev:
	cd frontend && npm run e2e

ci: test lint e2e

docker-clean:
	docker container prune -f --filter "until=24h"
