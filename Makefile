VENV ?= .venv
PYTHON_VERSION ?= 3.13
.PHONY: init clean

.create-venv:
	test -d $(VENV) || python$(PYTHON_VERSION) -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install poetry

.install-deps:
	$(VENV)/bin/poetry install

.install-pre-commit:
	$(VENV)/bin/poetry run pre-commit install

init:
	@echo "Creating virtual environment..."
	@$(MAKE) .create-venv
	@echo "Installing dependencies..."
	@$(MAKE) .install-deps
	@echo "Installing pre-commit hooks..."
	@$(MAKE) .install-pre-commit


clean:
	rm -rf .venv
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf .mypy_cache
	rm -rf dist
	rm -rf *.egg-info

pretty:
	$(VENV)/bin/ruff check --fix-only .
	$(VENV)/bin/ruff format .

mypy:
	$(VENV)/bin/mypy --install-types --non-interactive .

.ruff-lint:
	$(VENV)/bin/ruff check .


lint: mypy .ruff-lint
