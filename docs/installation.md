# Installation

## Requirements

- Python 3.12+
- Git
- `uv`
- PostgreSQL (or a hosted PostgreSQL database such as Neon)

## 1. Clone the repository

```bash
git clone <repository-url>
cd <project-directory>
```

## 2. Create the environment

Using `uv`:

```bash
uv sync
```

Activate the environment if needed:

```bash
source .venv/bin/activate
```

## 3. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DATABASE_URL=postgresql://user:password@host/database?sslmode=require
```

Replace `DATABASE_URL` with your PostgreSQL/Neon connection string.

## 4. Run migrations

```bash
uv run python manage.py migrate
```

## 5. Create an admin user

```bash
uv run python manage.py createsuperuser
```

Follow the prompts to create your account.

## 6. Start the development server

```bash
uv run python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Troubleshooting

If dependencies or the environment are missing, run:

```bash
uv sync
```

If database changes were made:

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

For production deployment, set `DEBUG=False` and configure the appropriate production environment variables.
