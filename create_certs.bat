@echo off
setlocal enabledelayedexpansion

:: Define color codes
set YELLOW=^[[33m
set GREEN=^[[32m
set NC=^[[0m

:: Check if the certificates already exist
if exist ".certs\server.key" if exist ".certs\server.crt" (
    echo %YELLOW%🔐 Certificates already exist.%NC%
    exit /b 0
) else (
    echo %YELLOW%🔐 Generating certificates...%NC%
    
    :: Create the certs directory if it doesn't exist
    if not exist ".certs" mkdir .certs

    :: Generate CA private key and certificate
    openssl genrsa -out .certs\ca.key 2048
    openssl req -x509 -new -nodes -key .certs\ca.key -subj "/CN=Ajna MAF 1" -days 365 -out .certs\ca.crt

    :: Generate server private key
    openssl genrsa -out .certs\server.key 2048

    :: Generate a Certificate Signing Request (CSR) for localhost
    openssl req -new -key .certs\server.key -subj "/CN=localhost" -out .certs\server.csr

    :: Sign the CSR with the CA to create the server certificate
    openssl x509 -req -in .certs\server.csr -CA .certs\ca.crt -CAkey .certs\ca.key -CAcreateserial -out .certs\server.crt -days 365
    
    echo %GREEN%🔐 Certificates generated.%NC%
)
