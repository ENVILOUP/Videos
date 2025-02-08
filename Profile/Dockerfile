FROM python:3.10.15-bullseye

WORKDIR /app/

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

ENV DATABASE_CONNECTION_URL=postgresql://postgres:postgres@pg/contentdb

COPY ./pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir poetry==1.8.4 \
    && poetry install --no-interaction --no-ansi

COPY ./app /app/app/
COPY ./migrations /app/migrations/

EXPOSE 8080

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]