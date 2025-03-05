# Use official Python image as a base
FROM python:3.11.11-slim AS base

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    libglib2.0-0 \
    libnss3 \
    libnss3-tools \
    libsm6 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libexpat1 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install uv first
RUN pip install uv

# Install playwright dependencies
RUN uv pip install --system playwright
RUN playwright install

# Install custom libraries
COPY *.whl ./
# Install custom dependencies
#RUN uv pip install /app/autogen_core-0.4.2-py3-none-any.whl /app/autogen_ext-0.4.2-py3-none-any.whl /app/autogen_magentic_one-0.0.1-py3-none-any.whl
RUN uv pip install --system autogen_core-0.4.2-py3-none-any.whl autogen_ext-0.4.2-py3-none-any.whl autogen_magentic_one-0.0.1-py3-none-any.whl


# Install dependencies in a single layer. Copy and install dependencies in a single step to optimize caching
COPY requirements.txt  ./
#RUN uv pip install --system -r requirements.txt autogen_core-0.4.2-py3-none-any.whl autogen_ext-0.4.2-py3-none-any.whl autogen_magentic_one-0.0.1-py3-none-any.whl
RUN uv pip install --system -r requirements.txt

# Copy the project files after dependencies are installed
COPY . .

# Generate self-signed SSL certificate (for development use only), replace these with your own certificates
RUN openssl req -x509 -newkey rsa:4096 -keyout /app/ssl.key -out /app/ssl.crt -days 3650 -nodes -subj "/CN=localhost"

# Expose the port FastAPI runs on
EXPOSE 8000

# Create a startup script to calculate CPU-based workers & threads dynamically
RUN echo '#!/bin/bash' > /start.sh && \
    echo 'CPU_CORES=$(nproc --all)' >> /start.sh && \
    echo 'WORKERS=$((2 * CPU_CORES + 1))' >> /start.sh && \
    echo 'THREADS=$((CPU_CORES * 2))' >> /start.sh && \
    echo 'echo "🚀 Starting FastAPI with $WORKERS workers and $THREADS threads"' >> /start.sh && \
    echo 'exec gunicorn -w $WORKERS --threads $THREADS -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --certfile /app/ssl.crt --keyfile /app/ssl.key app.main:app' >> /start.sh && \
    chmod +x /start.sh

# Set the startup script as CMD
CMD ["/bin/bash", "/start.sh"]