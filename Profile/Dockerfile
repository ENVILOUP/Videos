FROM python:3.10.15-bullseye

WORKDIR /app/

ENV PYTHONPATH /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

COPY ./pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir poetry==1.8.4 \
    && poetry install

COPY ./app /app/app/

EXPOSE 8080

ENTRYPOINT ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8080"]