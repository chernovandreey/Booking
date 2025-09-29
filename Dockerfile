# ---- base ----
FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"
WORKDIR /app

# системные пакеты для psycopg2 и сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# ---- deps ----
FROM base AS deps
# ставим Poetry (user install)
RUN curl -sSL https://install.python-poetry.org | python -
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# ---- app ----
FROM deps AS app
COPY . /app

EXPOSE 9000
# CMD не указываем — зададим команду в docker-compose.yml
