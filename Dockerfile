FROM node:23.6.0-bookworm-slim AS assets

WORKDIR /app/assets

ARG UID=1000
ARG GID=1000

RUN groupmod -g "${GID}" node && usermod -u "${UID}" -g "${GID}" node \
    && mkdir -p ./node_modules && chown node:node -R ./node_modules /app/assets

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN npm i -g corepack@latest && corepack enable 
# TODO https://github.com/nodejs/corepack/issues/612

USER node

ARG NODE_ENV="production"
ENV NODE_ENV="${NODE_ENV}" \
    USER="node"

COPY --chown=node:node ./assets /app/assets
COPY --chown=node:node ./src /app/src

 
RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --frozen-lockfile


###############################################################################

FROM assets AS assets_builder

RUN pnpm run build

###############################################################################

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS app_builder

# Build argument to control dev dependencies
ARG UV_INSTALL_DEV=false

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN groupadd -g "${GID}" app \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" app \
  && mkdir -p /app/staticfiles \
  && chown app:app -R /app/staticfiles /app

USER app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    if [ "$UV_INSTALL_DEV" = "false" ] || [ "$UV_INSTALL_DEV" = "0" ]; then \
        uv sync --frozen --no-install-project --no-dev; \
    else \
        uv sync --frozen --no-install-project --group dev --group test; \
    fi

COPY ./src /app/src

###############################################################################

FROM python:3.13-slim-bookworm AS app_dev

# Copy the application from the builder
COPY --from=app_builder --chown=app:app /app /app
RUN mkdir -p /app/assets_dist \
    chown app:app /app/assets_dist

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH" \
    USER="app"

WORKDIR /app/src

ARG DJANGO_DEBUG=false

CMD ["granian", "--interface", "asgi", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]

###############################################################################

FROM python:3.13-slim-bookworm

# Copy the application from the builder
COPY --from=app_builder --chown=app:app /app /app
COPY --from=assets_builder --chown=app:app /app/src/assets_dist /app/src/assets_dist

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH" \
    USER="app"

WORKDIR /app/src

RUN DJANGO_SECRET_KEY=dummyvalue python3 manage.py collectstatic --no-input

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python3 -c "import requests; requests.get('http://localhost:8000/admin/', timeout=30)"

CMD ["granian", "--interface", "asgi", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]