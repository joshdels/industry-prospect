.PHONY: run migrate

run:
	uv run python manage.py runserver


migrate:
	uv run python manage.py makemigrations
	uv run python manage.py migrate
	uv run python manage.py showmigrations
	

test:
	uv run python manage.py test


dev:
	uv run mcp dev apps/mcp/server.py

install:
	uv run mcp install apps/mcp/server.py \
		--with django \
		--with dj-database-url \
		--with psycopg[binary] \
		--with python-dotenv

kill:
	pkill -f claude


lint:
	uv run djlint . --reformat


celery:
	uv run celery -A config worker --loglevel=INFO --concurrency=1 --prefetch-multiplier=1 --max-tasks-per-child=2