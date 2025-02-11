# https://github.com/casey/just

dev-sync:
	uv sync --all-extras --no-cache

prod-sync:
	uv sync --no-dev --cache-dir .uv_cache

lint:
	uv run ruff format
	uv run ruff check --fix
	uv run mypy --install-types --non-interactive --package hackathon

start-neo4j:
	docker run --name neo4j -p 7474:7474 -p 7687:7687 -d -e NEO4J_AUTH=neo4j/password -e NEO4J_PLUGINS=\[\"apoc\"\] --rm neo4j:latest

stop-neo4j:
	docker stop neo4j

