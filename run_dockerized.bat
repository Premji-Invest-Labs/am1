@echo off
setlocal EnableDelayedExpansion

REM Run certificate creation
call create_certs.bat

REM Print banner
echo.
echo ╔═══════════════════════════════════════════════╗
echo ║                                               ║
echo ║   🚀 AM1 Application Stack Runner             ║
echo ║                                               ║
echo ╚═══════════════════════════════════════════════╝
echo.

REM Function to check if Docker is running
:check_docker
docker info > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [31m❌ Docker is not running. Please start Docker and try again.[0m
    exit /b 1
)

REM Function to handle project setup
:setup
echo [33m📦 Setting up project dependencies...[0m
    
REM Ensure directories exist
if not exist "backend\app\db\migrations" mkdir "backend\app\db\migrations"
    
echo [32m✅ Setup complete![0m
goto :eof

REM Function to stop all containers
:stop
echo [33m🛑 Stopping all containers...[0m
docker-compose down
echo [32m✅ All containers stopped.[0m
goto :eof

REM Function to rebuild all containers
:rebuild
echo [33m🔄 Rebuilding all containers...[0m
docker-compose build --no-cache
echo [32m✅ Rebuild complete![0m
goto :eof

REM Function to start all containers
:start
echo [33m🚀 Starting all services...[0m
docker-compose up -d
echo [32m✅ All services started![0m

echo [33m⏳ Waiting for services to be ready...[0m
timeout /t 5 /nobreak > nul

echo [34m================================================[0m
echo [32m🌐 Services are running:[0m
echo   [34mFrontend:[0m https://localhost:3000
echo   [34mBackend API:[0m https://localhost:8000/docs
echo   [34mDatabase:[0m localhost:5432
echo [34m================================================[0m
goto :eof

REM Function to display logs
:logs
echo [33m📋 Showing logs...[0m
docker-compose logs -f
goto :eof

REM Parse command line arguments
if "%1"=="" goto :usage
if "%1"=="setup" (
    call :check_docker
    call :setup
) else if "%1"=="start" (
    call :check_docker
    call :setup
    call :start
) else if "%1"=="stop" (
    call :check_docker
    call :stop
) else if "%1"=="restart" (
    call :check_docker
    call :stop
    call :start
) else if "%1"=="rebuild" (
    call :check_docker
    call :stop
    call :rebuild
    call :start
) else if "%1"=="logs" (
    call :check_docker
    call :logs
) else (
    goto :usage
)
goto :eof

:usage
echo [34mUsage:[0m %0 {setup^|start^|stop^|restart^|rebuild^|logs}
echo   [33msetup[0m    - Prepare project directories and files
echo   [33mstart[0m    - Start all services
echo   [33mstop[0m     - Stop all services
echo   [33mrestart[0m  - Restart all services
echo   [33mrebuild[0m  - Rebuild all containers from scratch
echo   [33mlogs[0m     - Show container logs
exit /b 1

:eof
endlocal