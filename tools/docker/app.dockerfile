FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

RUN apk add --no-cache postgresql-client
# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY ../.. /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src:$PYTHONPATH"
# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

RUN ["chmod", "+x", "/app/entrypoint.local.sh"]

CMD ["/app/entrypoint.local.sh"]

EXPOSE 8000

