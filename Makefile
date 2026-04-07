SERVICE = api

# Code style checks (run inside Docker)
lint:
	docker compose exec $(SERVICE) ruff check src/ scripts/

lint-fix:
	docker compose exec $(SERVICE) ruff check --fix src/ scripts/

format:
	docker compose exec $(SERVICE) ruff format src/ scripts/

format-check:
	docker compose exec $(SERVICE) ruff format --check src/ scripts/

type-check:
	docker compose exec $(SERVICE) mypy src/ --ignore-missing-imports

# Run all checks
check: format-check lint type-check

.PHONY: lint lint-fix format format-check type-check check
