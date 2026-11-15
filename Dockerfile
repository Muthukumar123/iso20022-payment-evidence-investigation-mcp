# Reproducible stdio MCP runtime for local use and Glama source introspection.
# This image does not expose a network port or connect to banking systems.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /opt/iso20022-mcp
COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN python -m pip install --no-cache-dir .

# The unprivileged process only reads synthetic/user-supplied XML via stdio.
RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin mcpuser
USER 10001:10001

ENTRYPOINT ["iso20022-mcp"]
