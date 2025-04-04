.PHONY: init clean

init:
	python3 -m venv .venv
	. .venv/bin/activate && \
	pip install --upgrade pip && \
	pip install poetry && \
	poetry install

clean:
	rm -rf .venv
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf .mypy_cache
	rm -rf dist
	rm -rf *.egg-info

make pretty:
	ruff format
	ruff check --fix --exit-zero
