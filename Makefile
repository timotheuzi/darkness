# DarknessMUD Django Makefile

.PHONY: help setup lint clean migrate init run repair stop test

PYTHON := python3
MANAGE := $(PYTHON) manage.py
SETTINGS := darkness_django.settings.local

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Install dependencies
	$(PYTHON) -m pipx install requirements/dev.txt

lint: ## Run static analysis
	@echo "Running lint (flake8)..."
	flake8 . --exclude=*/migrations/*,*/settings/*
	@echo "Running type check (optional)..."
	# mypy .

clean: ## Clean python cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov

migrate: ## Run database migrations
	$(MANAGE) makemigrations --settings=$(SETTINGS)
	$(MANAGE) migrate --settings=$(SETTINGS)

init: migrate ## Initialize game world data
	$(MANAGE) init_game --settings=$(SETTINGS)

run: stop migrate ## Run the Django development server
	$(MANAGE) runserver 0.0.0.0:8008 --settings=$(SETTINGS)

repair: stop ## Reset database and migrations
	rm -f db.sqlite3
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	$(MAKE) init
	@echo "Environment reset and re-initialized."

stop: ## Kill running django processes
	@pkill -f runserver || true

test: ## Run django tests
	$(MANAGE) test --settings=$(SETTINGS)
