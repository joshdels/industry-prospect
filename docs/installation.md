# Installation & Getting Started

This guide explains how to set up **Industry Prospect** for local development and how to run its Django and MCP components.

## Requirements

Make sure the following are installed:

* Python `3.14+`
* [`uv`](https://docs.astral.sh/uv/)
* PostgreSQL
* Git

The project currently requires:

```text
Python >= 3.14
Django >= 6.1.1
```

---

## 1. Clone the Repository

```bash
git clone <repository-url>
cd industry-prospect
```

---

## 2. Install Dependencies

This project uses `uv` for dependency management.

Install the project dependencies:

```bash
uv sync
```

Development dependencies can also be installed with:

```bash
uv sync --dev
```

The main dependencies include:

* Django
* Celery
* MCP
* python-dotenv

---

## 3. Environment Variables

Create a `.env` file in the project root.

Example:

```env
DJANGO_SETTINGS_MODULE=config.settings

# Database
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE

# AI / external services
# Add required API keys here
```

Do not commit `.env` to Git.

Make sure it is included in `.gitignore`:

```gitignore
.env
```

---

## 4. Database Setup

Industry Prospect uses PostgreSQL for persistent data.

Create your PostgreSQL database and configure the connection through your environment variables.

Then run Django migrations:

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

Check migration status:

```bash
uv run python manage.py showmigrations
```

---

## 5. Create a Superuser

To access the Django admin:

```bash
uv run python manage.py createsuperuser
```

Follow the prompts to create your administrator account.

---

## 6. Run the Django Development Server

Start the application:

```bash
uv run python manage.py runserver
```

Django will start the development server and display the local address in the terminal.

---

# Development Commands

The project includes a `Makefile` for common development commands.

## Run the Application

```bash
make run
```

Equivalent to:

```bash
uv run python manage.py runserver
```

---

## Run Migrations

```bash
make migrate
```

This runs:

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py showmigrations
```

---

## Run Tests

```bash
make test
```

Or directly:

```bash
uv run python manage.py test
```

---

## Format Django Templates

```bash
make lint
```

This runs:

```bash
uv run djlint . --reformat
```

---

# MCP Development

Industry Prospect exposes functionality through an MCP server so an AI client can interact with the application.

The MCP server is located at:

```text
apps/mcp/server.py
```

## Run MCP in Development

```bash
make dev
```

Equivalent to:

```bash
uv run mcp dev apps/mcp/server.py
```

This is useful when developing and testing MCP tools locally.

---

# Install MCP for Claude Desktop

To install the MCP server for Claude Desktop:

```bash
make install
```

The underlying command is:

```bash
uv run mcp install apps/mcp/server.py \
    --with django \
    --with celery \
    --with python-dotenv
```

After installation, restart Claude Desktop if necessary.

The MCP server should then be available to Claude.

---

# Celery

Celery is used for background processing.

Start a worker with:

```bash
make celery
```

Equivalent to:

```bash
uv run celery -A config worker \
    --loglevel=INFO \
    --concurrency=1 \
    --prefetch-multiplier=1 \
    --max-tasks-per-child=2
```

Keep the Celery worker running in a separate terminal while developing features that use background tasks.

---

# Useful Workflow

A typical development session looks like:

### Terminal 1 — Django

```bash
make run
```

### Terminal 2 — Celery

```bash
make celery
```

### Terminal 3 — MCP development

```bash
make dev
```

Then use the Django application and your MCP client to test the complete workflow.

---

# Common Commands

| Command        | Purpose                               |
| -------------- | ------------------------------------- |
| `make run`     | Start Django development server       |
| `make migrate` | Create and apply migrations           |
| `make test`    | Run Django tests                      |
| `make dev`     | Start MCP development server          |
| `make install` | Install MCP server for Claude Desktop |
| `make celery`  | Start Celery worker                   |
| `make lint`    | Format Django templates               |

---

# Project Configuration

The project configuration is primarily defined in:

```text
pyproject.toml
```

Current project requirements:

```toml
[project]
name = "industry-prospect"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = [
    "celery>=5.6.3",
    "django>=6.1.1",
    "mcp[cli]>=2.1.1",
    "python-dotenv>=1.2.3",
]

[dependency-groups]
dev = [
    "djlint>=1.45.2",
]
```

---

# Troubleshooting

## Django cannot connect to PostgreSQL

Check:

1. PostgreSQL is running.
2. The database exists.
3. Your database credentials are correct.
4. Your environment variables are loaded.
5. The configured database URL is correct.

---

## Migrations are missing

Run:

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

Then check:

```bash
uv run python manage.py showmigrations
```

---

## MCP changes are not appearing

When developing the MCP server, restart the MCP development process:

```bash
make dev
```

For Claude Desktop, restart Claude Desktop after changing the installed MCP configuration or server.

---

## Celery tasks are not running

Make sure the Celery worker is running:

```bash
make celery
```

Keep it running in a separate terminal from Django.
