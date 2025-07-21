check:
	@python scripts/ensure_single_module.py
	ruff check .
	mypy .
	pytest -q