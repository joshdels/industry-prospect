.PHONY: run migrate

run:
	python manage.py runserver


migrate:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py showmigrations
	

dev:
	uv run mcp dev app/server/server.py


install:
	uv run mcp install app/server/server.py


lint:
	uv run djlint . --reformat


celery:
	celery -A config worker --loglevel=INFO --concurrency=1 --prefetch-multiplier=1 --max-tasks-per-child=2