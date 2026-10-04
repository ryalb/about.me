# syntax=docker/dockerfile:1
FROM python:3.13-slim-bookworm

# WeasyPrint native libs (Pango/HarfBuzz/Cairo stack) + fonts for PDF rendering.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpango-1.0-0 \
        libpangoft2-1.0-0 \
        libharfbuzz-subset0 \
        libcairo2 \
        libgdk-pixbuf-2.0-0 \
        shared-mime-info \
        fontconfig \
        fonts-liberation \
        fonts-dejavu-core \
        fonts-noto-core \
    && rm -rf /var/lib/apt/lists/*

# Iosevka Term Slab (the theme's primary face), resolved through fontconfig.
COPY fonts /usr/local/share/fonts/iosevka
RUN fc-cache -f

# uv (Python deps) and Bun (jsonresume theme rendering) from their official images.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/
COPY --from=oven/bun:1.3.5 /usr/local/bin/bun /usr/local/bin/bun

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Python dependencies (cached until pyproject.toml / uv.lock change).
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# JS dependencies: npm jsonresume themes and the custom `base` theme.
COPY node/package.json node/bun.lock ./node/
RUN cd node && bun install --frozen-lockfile
COPY custom/themes/base/package.json custom/themes/base/bun.lock ./custom/themes/base/
RUN cd custom/themes/base && bun install --frozen-lockfile

# Project sources.
COPY resume_generator ./resume_generator
COPY node/render_theme.mjs ./node/
COPY custom ./custom
COPY scripts ./scripts
COPY src ./src
RUN uv sync --frozen

# Generated files land here; mount a host directory to collect them.
VOLUME /app/.output

ENTRYPOINT ["resume"]
CMD ["--help"]
