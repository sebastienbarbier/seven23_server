FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.12.1 /uv /uvx /bin/

WORKDIR /app
RUN mkdir /app/collectstatic /opt/venv

RUN adduser --disabled-password --gecos "" seven23
RUN chown seven23:seven23 /app /app/collectstatic /opt/venv
VOLUME /app/collectstatic

# Keep the virtualenv outside /app so bind-mounting the project does not hide it.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

RUN apt-get update && \
 apt-get install -y --no-install-recommends \
   libpq5 libjpeg62-turbo zlib1g libffi8 && \
 apt-get install -y --no-install-recommends \
   gcc g++ libpq-dev libjpeg-dev zlib1g-dev libffi-dev && \
 rm -rf /var/lib/apt/lists/*

COPY --chown=seven23 pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

COPY --chown=seven23 . .

RUN apt-get update && \
 apt-get purge -y --auto-remove gcc g++ libpq-dev libjpeg-dev zlib1g-dev libffi-dev && \
 rm -rf /var/lib/apt/lists/*

USER seven23
EXPOSE 8000

ENTRYPOINT [ "/app/docker/entrypoint.sh" ]
