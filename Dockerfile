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
    PATH="/opt/dart-sass:/opt/venv/bin:$PATH"

# Dart Sass standalone binary (replaces heavy libsass / C++ toolchain).
ARG TARGETARCH
ARG SASS_VERSION=1.102.0
RUN case "$TARGETARCH" in \
      amd64) SASS_ARCH=x64 ;; \
      arm64) SASS_ARCH=arm64 ;; \
      *) echo "Unsupported arch: $TARGETARCH" >&2; exit 1 ;; \
    esac \
 && apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl libpq5 \
 && curl -fsSL "https://github.com/sass/dart-sass/releases/download/${SASS_VERSION}/dart-sass-${SASS_VERSION}-linux-${SASS_ARCH}.tar.gz" \
    | tar -xz -C /opt \
 && apt-get purge -y --auto-remove curl \
 && rm -rf /var/lib/apt/lists/*

COPY --chown=seven23 pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

COPY --chown=seven23 . .

USER seven23
EXPOSE 8000

ENTRYPOINT [ "/app/docker/entrypoint.sh" ]
