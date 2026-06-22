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

venv: $(VENV)/bin/python ## Create virtual environment

$(VENV)/bin/python:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip

setup: $(VENV)/bin/python ## Install dependencies
	$(PYTHON) -m pip install -r requirements/dev.txt

clean: setup ## Clean cache, database, and migrations, then recreate a blank DB with latest models
	@echo "Cleaning generated files..."
	# Skip .venv directory and delete __pycache__ and .pyc files
	find . -name "$(VENV)" -prune -o -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "$(VENV)" -prune -o -type f -name "*.pyc" -exec rm -f {} +
	rm -rf .pytest_cache .coverage htmlcov staticfiles db.sqlite3
	@echo "Cleaning app migrations..."
	# Explicitly delete all numbered migrations (including 0001_initial.py) to avoid collisions
	find . -name "$(VENV)" -prune -o -path "*/migrations/*.py" -not -name "__init__.py" -exec rm -f {} +
	@echo "Recreating blank database with latest models..."
	$(MANAGE) makemigrations game --settings=$(SETTINGS)
	$(MANAGE) makemigrations --settings=$(SETTINGS)
	$(MANAGE) migrate --settings=$(SETTINGS)

migrate: setup ## Run database migrations (local)
	$(MANAGE) makemigrations game --settings=$(SETTINGS)
	$(MANAGE) makemigrations --settings=$(SETTINGS)
	$(MANAGE) migrate --settings=$(SETTINGS)

init: migrate ## Initialize game world data (local)
	$(MANAGE) init_game --settings=$(SETTINGS)

deploy-migrate: ## Run database migrations (PythonAnywhere/production)
	$(PYTHONANYWHERE_MANAGE) makemigrations game --settings=$(PYTHONANYWHERE_SETTINGS)
	$(PYTHONANYWHERE_MANAGE) makemigrations --settings=$(PYTHONANYWHERE_SETTINGS)
	$(PYTHONANYWHERE_MANAGE) migrate --settings=$(PYTHONANYWHERE_SETTINGS)

deploy-init: deploy-migrate ## Initialize game world data (PythonAnywhere/production)
	$(PYTHONANYWHERE_MANAGE) init_game --settings=$(PYTHONANYWHERE_SETTINGS)

run: clean init ## Full clean, build/initialize, and run the Django development server
	$(MANAGE) runserver 0.0.0.0:8008 --settings=$(SETTINGS)

deploy-run: ## Run the Django development server (PythonAnywhere/production)
	$(PYTHONANYWHERE_MANAGE) runserver 0.0.0.0:8008 --settings=$(PYTHONANYWHERE_SETTINGS)

repair: ## Deep repair: Nuke venv and start over
	@echo "Performing deep repair..."
	rm -rf $(VENV)
	$(MAKE) run

test: setup ## Run django tests
	$(MANAGE) test --settings=$(SETTINGS)

lint: setup ## Run static analysis
	@echo "Running lint (flake8)..."
	$(PYTHON) -m flake8 . --exclude=*/migrations/*,*/settings/*,$(VENV)/*
