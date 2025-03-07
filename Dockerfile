FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

CMD /app/.venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:"${PORT}"
#CMD ["/app/.venv/bin/gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8080"]

EXPOSE "${PORT}"