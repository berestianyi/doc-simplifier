FROM python:3.12-slim-bullseye

LABEL authors="ivan.berestianyi"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/src/app/src

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /usr/src/app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-root --no-dev

COPY . .

WORKDIR /usr/src/app/src


EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]