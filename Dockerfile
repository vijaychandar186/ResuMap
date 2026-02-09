FROM python:3.12-slim

WORKDIR /app

# Install build tools for llama-cpp-python compilation and uv
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ cmake make && \
    pip install --no-cache-dir uv && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency files first for layer caching
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen

# Copy application code
COPY app/ ./app/
COPY scripts/ ./scripts/

# Download model at build time so it's baked into the image
RUN /app/.venv/bin/python -m scripts.download_model

ENV RESUMAP_MODEL_N_CTX=8192
ENV RESUMAP_MODEL_N_THREADS=4

EXPOSE 8000

CMD ["/app/.venv/bin/python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]