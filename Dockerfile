FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --only main --no-root

COPY . .

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]