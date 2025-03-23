# Use official Python image as a base
FROM python:3.12-bookworm AS base
#FROM mcr.microsoft.com/playwright/python:v1.50.0-noble AS base

# Set the working directory inside the container
WORKDIR /app
# Install CA certificates (for SSL verification)
# Install system dependencies
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    apt-transport-https \
#    ca-certificates \
#    libglib2.0-0 \
#    libnss3 \
#    libnss3-tools \
#    libsm6 \
#    libnspr4 \
#    libdbus-1-3 \
#    libatk1.0-0 \
#    libatk-bridge2.0-0 \
#    libcups2 \
#    libexpat1 \
#    libx11-6 \
#    libxcomposite1 \
#    libxdamage1 \
#    libxext6 \
#    libxfixes3 \
#    libxrandr2 \
#    libgbm1 \
#    libxcb1 \
#    libxkbcommon0 \
#    libpango-1.0-0 \
#    libcairo2 \
#    libasound2 \
#    libatspi2.0-0 \
#    && rm -rf /var/lib/apt/lists/* \
#
#RUN apt-get update && apt-get install -y \
#    libx11-xcb1 \
#    libxcursor1 \
#    libgtk-3-0 \
#    libpangocairo-1.0-0 \
#    libcairo2 \
#    libgdk-pixbuf2.0-0 \
#    && apt-get clean

ENV PATH="/root/.cargo/bin:${PATH}"
# RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates

# Install uv first
RUN pip install uv
# RUN curl -sSL https://astral.sh/uv/install.sh | bash

# Install Playwright dependencies
# RUN uv pip install --system playwright
# RUN playwright install
RUN uv pip install --system playwright==1.50.0 && \
    playwright install --with-deps chromium

# Copy custom libraries
COPY backend/whl/*.whl /app/

# Install custom dependencies
RUN uv pip install --system /app/autogen_core-0.4.2-py3-none-any.whl \
                             /app/autogen_ext-0.4.2-py3-none-any.whl \
                             /app/autogen_magentic_one-0.0.1-py3-none-any.whl

# Copy the requirements file
COPY backend/requirements_stable.txt /app/

# Install dependencies
RUN uv pip install --system -r /app/requirements_stable.txt

# Invalidate the cache when the requirements file changes
#ARG CACHEBUST=1
# Copy the actual application code correctly
COPY backend/.env /app/
COPY backend/app /app/app
COPY backend/config /app/config
COPY backend/tests /app/tests

# Install curl and other necessary tools
#RUN apt-get update && \
#    apt-get install -y curl libnss3-tools && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*
#RUN apt update
#RUN apt install -y libnss3-tools
#RUN curl -sSL https://github.com/FiloSottile/mkcert/releases/latest/download/mkcert-v1.4.4-linux-amd64 -o mkcert
#RUN mv mkcert /usr/local/bin/
#RUN chmod +x /usr/local/bin/mkcert
#RUN mkcert -install
#RUN mkcert -cert-file /etc/ssl/certs/pi-cert.pem -key-file /etc/ssl/certs/pi-key.pem localhost
COPY .certs/server.crt /etc/ssl/certs/pi-localhost.crt
COPY .certs/server.key /etc/ssl/certs/pi-localhost.key
#RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

## Generate self-signed SSL certificate if not provided
#RUN if [ ! -f "/app/.certs/key.pem" ]; then \
#    echo "Generating self-signed SSL certificate"; \
#    mkdir -p /app/.certs; \
#    openssl req -x509 -newkey rsa:4096 -keyout /app/.certs/dummy-localhost.key -out /app/.certs/cert.pem -days 3650 -nodes -subj "/CN=localhost"; \
#    cat /app/.certs/cert.pem /app/.certs/dummy-localhost.key > /app/.certs/dummy-localhost.pem; \
#    fi
# Install necessary packages to update CA certificates

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy SSL certificates into the container
#COPY .certs/pi-cert.pem /etc/ssl/certs/pi-cert.pem
#COPY .certs/pi-key.pem /etc/ssl/certs/pi-key.pem
#COPY .certs/pi-pem.pem /etc/ssl/certs/pi-pem.pem
#COPY .certs/pi-cert.crt /etc/ssl/certs/pi-cert.crt

## Ensure the SSL certificates are recognized inside the container
#COPY .certs/pi-cert.pem /usr/local/share/ca-certificates/pi-pem.pem
#RUN chmod 644 /usr/local/share/ca-certificates/pi-pem.pem
COPY .certs/server.crt /usr/local/share/ca-certificates/pi-localhost.crt
#RUN chmod 644 /usr/local/share/ca-certificates/pi-localhost.crt
RUN chmod 644 /usr/local/share/ca-certificates/*.crt
RUN update-ca-certificates

# Add this crucial step - append your cert to the certifi bundle
RUN cat /usr/local/share/ca-certificates/pi-localhost.crt >> $(python -m certifi)
#ENV PYTHONWARNINGS="ignore:Unverified HTTPS request"
#ENV PYTHONHTTPSVERIFY=0

# Copy the self-signed certificate
#COPY .certs/pi-cert.pem /usr/local/share/ca-certificates/pi-cert.crt

# Set permissions and update CA certificates
#RUN chmod 644 /usr/local/share/ca-certificates/pi-cert.crt
#RUN update-ca-certificates

## Set OpenSSL and Python to trust the cert
# Additional measures for OpenSSL and Python to trust the certificates
#ENV SSL_CERT_FILE=/etc/ssl/certs/pi-cert.pem
#ENV SSL_KEY_FILE=/etc/ssl/certs/pi-key.pem
#ENV SSL_CERT_FILE=/etc/ssl/certs/pi-localhost.crt
#ENV SSL_KEY_FILE=/etc/ssl/certs/pi-localhost.key
#ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/pi-localhost.crt

ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

#ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
#ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
#ENV HTTPX_SSL_VERIFY="/etc/ssl/certs/pi-cert.pem"
#ENV NODE_EXTRA_CA_CERTS="/etc/ssl/certs/pi-cert.pem"
#ENV CURL_CA_BUNDLE="/etc/ssl/certs/pi-cert.pem"
#ENV OPENAI_VERIFY_SSL_CERTS=true

# Create directories for SSL certificates in Python
#RUN mkdir -p /usr/local/lib/python3.12/site-packages/certifi
#COPY .certs/pi-cert.pem /usr/local/lib/python3.12/site-packages/certifi/cacert.pem

# Expose the port FastAPI runs on
EXPOSE 8000

# Set the Python module path
#ENV PYTHONPATH="/app"

#ENV ENABLE_SSL=false

# Create a startup script to dynamically determine workers and optionally enable SSL
#RUN echo '#!/bin/bash' > /start.sh \
#    && echo 'CPU_CORES=$(nproc --all)' >> /start.sh \
#    && echo 'WORKERS=$((2 * CPU_CORES + 1))' >> /start.sh \
#    && echo 'THREADS=$((CPU_CORES * 2))' >> /start.sh \
#    && echo 'echo "🚀 Starting FastAPI with $WORKERS workers and $THREADS threads"' >> /start.sh \
#    && echo 'CMD="gunicorn -w $WORKERS --threads $THREADS -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 app.main:app"' >> /start.sh \
#    && echo 'if [ "$ENABLE_SSL" = "true" ]; then' >> /start.sh \
#    && echo '  CMD="$CMD --certfile /etc/ssl/certs/pi-cert.pem --keyfile /etc/ssl/certs/pi-key.pem"' >> /start.sh \
#    && echo '  echo "🔒 SSL enabled: Using certificate /etc/ssl/certs/pi-cert.pem"' >> /start.sh \
#    && echo 'fi' >> /start.sh \
#    && echo 'exec $CMD' >> /start.sh \
#    && chmod +x /start.sh

RUN echo '#!/bin/bash' > /start.sh && \
    echo 'CPU_CORES=$(nproc --all)' >> /start.sh && \
    echo 'WORKERS=$((2 * CPU_CORES + 1))' >> /start.sh && \
    echo 'THREADS=$((CPU_CORES * 2))' >> /start.sh && \
    echo 'echo "🚀 Starting FastAPI with $WORKERS workers and $THREADS threads"' >> /start.sh && \
    echo 'exec gunicorn -w $WORKERS --threads $THREADS -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000  \
    --certfile /etc/ssl/certs/pi-localhost.crt --keyfile /etc/ssl/certs/pi-localhost.key app.main:app' >> /start.sh && \
    chmod +x /start.sh

# Set the startup script as CMD
CMD ["/bin/bash", "/start.sh"]