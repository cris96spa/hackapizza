dev-sync:
	uv sync --all-extras --no-cache

prod-sync:
	uv sync --no-dev --cache-dir .uv_cache

lint:
	uv run ruff format
	uv run ruff check --fix
	uv run mypy --install-types --non-interactive --package hackathon