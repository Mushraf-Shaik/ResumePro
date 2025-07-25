#!/bin/bash

# ResumePro Docker Deployment Script
# Usage: ./deploy.sh [start|stop|restart|logs|build]

set -e

PROJECT_NAME="resumepro"
COMPOSE_FILE="docker-compose.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Check if .env file exists
check_env() {
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from template..."
        cp .env.docker .env
        print_warning "Please edit .env file with your actual API keys before starting the application."
        return 1
    fi
    return 0
}

# Start the application
start_app() {
    print_status "Starting ResumePro application..."
    check_docker
    if ! check_env; then
        print_error "Please configure .env file first."
        exit 1
    fi
    
    docker-compose -f $COMPOSE_FILE up -d --build
    
    print_status "Application started successfully!"
    print_status "Access your application at: http://localhost:5000"
    print_status "Health check: http://localhost:5000/health"
}

# Stop the application
stop_app() {
    print_status "Stopping ResumePro application..."
    check_docker
    docker-compose -f $COMPOSE_FILE down
    print_status "Application stopped successfully!"
}

# Restart the application
restart_app() {
    print_status "Restarting ResumePro application..."
    stop_app
    start_app
}

# Show logs
show_logs() {
    print_status "Showing application logs..."
    check_docker
    docker-compose -f $COMPOSE_FILE logs -f
}

# Build only
build_app() {
    print_status "Building ResumePro Docker image..."
    check_docker
    docker-compose -f $COMPOSE_FILE build --no-cache
    print_status "Build completed successfully!"
}

# Status check
status_check() {
    print_status "Checking application status..."
    check_docker
    
    if docker-compose -f $COMPOSE_FILE ps | grep -q "Up"; then
        print_status "Application is running"
        docker-compose -f $COMPOSE_FILE ps
        
        # Health check
        if curl -f http://localhost:5000/health > /dev/null 2>&1; then
            print_status "Health check: PASSED"
        else
            print_warning "Health check: FAILED"
        fi
    else
        print_warning "Application is not running"
    fi
}

# Production deployment
deploy_production() {
    print_status "Starting production deployment with Nginx..."
    check_docker
    if ! check_env; then
        print_error "Please configure .env file first."
        exit 1
    fi
    
    docker-compose -f $COMPOSE_FILE --profile production up -d --build
    
    print_status "Production deployment started successfully!"
    print_status "Access your application at: http://localhost:80"
    print_status "Direct app access: http://localhost:5000"
}

# Show help
show_help() {
    echo "ResumePro Docker Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start       Start the application"
    echo "  stop        Stop the application"
    echo "  restart     Restart the application"
    echo "  logs        Show application logs"
    echo "  build       Build Docker image"
    echo "  status      Check application status"
    echo "  production  Start with production configuration (Nginx)"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start                 # Start the application"
    echo "  $0 logs                  # View logs"
    echo "  $0 production           # Production deployment"
}

# Main script logic
case "${1:-help}" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    restart)
        restart_app
        ;;
    logs)
        show_logs
        ;;
    build)
        build_app
        ;;
    status)
        status_check
        ;;
    production)
        deploy_production
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
