@echo off
REM ResumePro Docker Deployment Script for Windows
REM Usage: deploy.bat [start|stop|restart|logs|build|status|production|help]

setlocal enabledelayedexpansion

set PROJECT_NAME=resumepro
set COMPOSE_FILE=docker-compose.yml

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Get command argument
set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=help

REM Execute command
if "%COMMAND%"=="start" goto start_app
if "%COMMAND%"=="stop" goto stop_app
if "%COMMAND%"=="restart" goto restart_app
if "%COMMAND%"=="logs" goto show_logs
if "%COMMAND%"=="build" goto build_app
if "%COMMAND%"=="status" goto status_check
if "%COMMAND%"=="production" goto deploy_production
if "%COMMAND%"=="help" goto show_help
if "%COMMAND%"=="--help" goto show_help
if "%COMMAND%"=="-h" goto show_help

echo [ERROR] Unknown command: %COMMAND%
goto show_help

:start_app
echo [INFO] Starting ResumePro application...

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found. Creating from template...
    copy .env.docker .env >nul
    echo [WARNING] Please edit .env file with your actual API keys before starting the application.
    echo [ERROR] Please configure .env file first.
    exit /b 1
)

docker-compose -f %COMPOSE_FILE% up -d --build
if errorlevel 1 (
    echo [ERROR] Failed to start application
    exit /b 1
)

echo [INFO] Application started successfully!
echo [INFO] Access your application at: http://localhost:5000
echo [INFO] Health check: http://localhost:5000/health
goto end

:stop_app
echo [INFO] Stopping ResumePro application...
docker-compose -f %COMPOSE_FILE% down
echo [INFO] Application stopped successfully!
goto end

:restart_app
echo [INFO] Restarting ResumePro application...
call :stop_app
call :start_app
goto end

:show_logs
echo [INFO] Showing application logs...
docker-compose -f %COMPOSE_FILE% logs -f
goto end

:build_app
echo [INFO] Building ResumePro Docker image...
docker-compose -f %COMPOSE_FILE% build --no-cache
echo [INFO] Build completed successfully!
goto end

:status_check
echo [INFO] Checking application status...
docker-compose -f %COMPOSE_FILE% ps

REM Check if containers are running
docker-compose -f %COMPOSE_FILE% ps | findstr "Up" >nul
if errorlevel 1 (
    echo [WARNING] Application is not running
) else (
    echo [INFO] Application is running
    
    REM Health check
    curl -f http://localhost:5000/health >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Health check: FAILED
    ) else (
        echo [INFO] Health check: PASSED
    )
)
goto end

:deploy_production
echo [INFO] Starting production deployment with Nginx...

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found. Creating from template...
    copy .env.docker .env >nul
    echo [WARNING] Please edit .env file with your actual API keys before starting the application.
    echo [ERROR] Please configure .env file first.
    exit /b 1
)

docker-compose -f %COMPOSE_FILE% --profile production up -d --build
if errorlevel 1 (
    echo [ERROR] Failed to start production deployment
    exit /b 1
)

echo [INFO] Production deployment started successfully!
echo [INFO] Access your application at: http://localhost:80
echo [INFO] Direct app access: http://localhost:5000
goto end

:show_help
echo ResumePro Docker Deployment Script for Windows
echo.
echo Usage: %0 [COMMAND]
echo.
echo Commands:
echo   start       Start the application
echo   stop        Stop the application
echo   restart     Restart the application
echo   logs        Show application logs
echo   build       Build Docker image
echo   status      Check application status
echo   production  Start with production configuration (Nginx)
echo   help        Show this help message
echo.
echo Examples:
echo   %0 start                 # Start the application
echo   %0 logs                  # View logs
echo   %0 production           # Production deployment
goto end

:end
endlocal
