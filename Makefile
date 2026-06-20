# DarknessMUD Django Makefile

.PHONY: help venv setup lint clean migrate init run repair test deploy-init

VENV := .venv
PYTHON := $(VENV)/bin/python
MANAGE := $(PYTHON) manage.py
SETTINGS := darkness_django.settings.local

# PythonAnywhere uses 'venv' instead of '.venv'
PYTHONANYWHERE_VENV := venv
PYTHONANYWHERE_PYTHON := $(PYTHONANYWHERE_VENV)/bin/python
PYTHONANYWHERE_MANAGE := $(PYTHONANYWHERE_PYTHON) manage.py
PYTHONANYWHERE_SETTINGS := darkness_django.settings.production

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

venv: ## Create virtual environment
	$(PYTHON) -m venv $(VENV)

setup: venv ## Install dependencies
	$(VENV)/bin/pip install -r requirements/dev.txt

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

migrate: ## Run database migrations (local)
	$(MANAGE) makemigrations --settings=$(SETTINGS)
	$(MANAGE) migrate --settings=$(SETTINGS)

init: migrate ## Initialize game world data (local)
	$(MANAGE) init_game --settings=$(SETTINGS)

deploy-migrate: ## Run database migrations (PythonAnywhere/production)
	$(PYTHONANYWHERE_MANAGE) makemigrations --settings=$(PYTHONANYWHERE_SETTINGS)
	$(PYTHONANYWHERE_MANAGE) migrate --settings=$(PYTHONANYWHERE_SETTINGS)

deploy-init: deploy-migrate ## Initialize game world data (PythonAnywhere/production)
	$(PYTHONANYWHERE_MANAGE) init_game --settings=$(PYTHONANYWHERE_SETTINGS)

run: migrate ## Run the Django development server
	$(MANAGE) runserver 0.0.0.0:8008 --settings=$(SETTINGS)

deploy-run: ## Run the Django development server (PythonAnywhere/production)
	$(PYTHONANYWHERE_MANAGE) runserver 0.0.0.0:8008 --settings=$(PYTHONANYWHERE_SETTINGS)

repair: #stop ## Reset database and migrations
	rm -f db.sqlite3
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	$(MAKE) init
	@echo "Environment reset and re-initialized."

#stop: ## Kill running django processes
#	@pkill -f runserver || true

test: ## Run django tests
	$(MANAGE) test --settings=$(SETTINGS)
