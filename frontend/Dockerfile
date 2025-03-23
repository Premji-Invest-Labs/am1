# Build stage
FROM node:20-slim AS build

# Set working directory
WORKDIR /app

# Invalidate the cache when the requirements file changes
#ARG CACHEBUST=1
# Copy package.json and package-lock.json from the frontend directory
COPY frontend/package*.json ./

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
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

#ENV DEBIAN_FRONTEND=noninteractive
### Debug: Check if package.json exists
##RUN ls -lah /app && cat /app/package.json
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    ca-certificates \
#    && rm -rf /var/lib/apt/lists/*

#RUN echo $(ls -1agh)
#RUN pwd
#RUN ls -1agh /etc/ssl/certs | grep pi-cert.pem
# Copy SSL certificates into the container
#COPY ../.certs/pi-cert.pem /etc/ssl/certs/pi-cert.pem
#COPY ../.certs/pi-key.pem /etc/ssl/certs/pi-key.pem
#COPY .certs/pi-pem.pem /etc/ssl/certs/pi-pem.pem

## Ensure the SSL certificates are recognized inside the container
COPY .certs/server.crt /usr/local/share/ca-certificates/pi-localhost.crt
RUN chmod 644 /usr/local/share/ca-certificates/pi-localhost.crt
RUN update-ca-certificates

# Install dependencies
RUN npm install --force

# Invalidate the cache when the requirements file changes
#ARG CACHEBUST=1
# Copy frontend files
COPY frontend ./

# Development stage
FROM node:20-slim AS development

WORKDIR /app

# Invalidate the cache when the requirements file changes
#ARG CACHEBUST=1
# Copy built frontend app from build stage
COPY --from=build /app .

# Install development dependencies (ensure everything is installed)
RUN npm install --force

# Expose port for Vite
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]