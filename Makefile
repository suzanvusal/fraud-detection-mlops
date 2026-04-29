.PHONY: up down test lint serve simulate

up:
	docker compose up -d
	@echo "✓ Stack started"

down:
	docker compose down -v

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	ruff check src/ tests/ --fix

serve:
	uvicorn src.serving.api:app --reload --port 8000

simulate:
	python -m src.ingestion.simulator --transactions 10000 --fraud-rate 0.05

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
