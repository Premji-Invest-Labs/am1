#!/bin/bash
echo "TODO: Fix run_dev.sh"
exit 1
bash create_certs.sh

set -e

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════╗"
echo "║                                               ║"
echo "║   🚀 AM1 Application Stack Runner             ║"
echo "║                                               ║"
echo "╚═══════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to check if Docker is running
check_docker() {
  if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
  fi
}

# Function to handle project setup
setup() {
  echo -e "${YELLOW}📦 Setting up project dependencies...${NC}"
  
  # Ensure directories exist for database migrations
  mkdir -p backend/app/db/migrations
  
#  # Move init.sql if it's in the old location and not in the new one
#  if [ -f "backend/app/repository/init.sql" ] && [ ! -f "backend/app/db/migrations/init.sql" ]; then
#    echo -e "${YELLOW}📂 Moving database setup script to new location...${NC}"
#    cp backend/app/repository/init.sql backend/app/db/migrations/init.sql
#  fi
  
  echo -e "${GREEN}✅ Setup complete!${NC}"
}

# Function to stop all containers
stop() {
  echo -e "${YELLOW}🛑 Stopping all containers...${NC}"
  docker-compose down
  echo -e "${GREEN}✅ All containers stopped.${NC}"
}

# Function to stop all containers and remove containers, networks, images, and volumes
clean_slate() {
  echo -e "${YELLOW}🧹 Cleaning up all containers, images, networks, and volumes...${NC}"
  docker-compose down -v --rmi all --remove-orphans
  echo -e "${GREEN}✅ Cleanup complete!${NC}"
}

# Function to build all containers from cached layers
cached_build() {
  echo -e "${YELLOW}🔄 Rebuilding all containers from cached layers...${NC}"
  docker-compose build
  echo -e "${GREEN}✅ Rebuild complete!${NC}"
}

# Function to build all containers from scratch
clean_build() {
  echo -e "${YELLOW}🔄 Rebuilding all containers from scratch...${NC}"
  docker-compose build --no-cache
  echo -e "${GREEN}✅ Rebuild complete!${NC}"
}

build() {
  ENABLE_CACHE=$1
  echo -e "${YELLOW}🚀 Building all services before starting...${NC}"
  if [ "$ENABLE_CACHE" == "disable" ]; then
    clean_build
  else
    cached_build
  fi
}

# Function to start all containers
start() {
  ENABLE_CACHE=$1
  echo -e "${YELLOW}🚀 Starting all services...${NC}"
  # Check if the container is already running
  if [ "$(docker ps --filter "name=am1" --format '{{.Names}}' | grep -c "am1")" -eq 3 ]; then
    echo -e "${GREEN}✅ Container is already running. Skipping build and starting container...${NC}"
    docker-compose start
  else
    build "$ENABLE_CACHE"
  fi
  echo -e "${GREEN}✅ All services started!${NC}"

  # Wait for services to be ready
  echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
  sleep 5

  # Print access information
  echo -e "${BLUE}================================================${NC}"
  echo -e "${GREEN}🌐 Services are running:${NC}"
  echo -e "  ${BLUE}Frontend:${NC} https://localhost:3000"
  echo -e "  ${BLUE}Backend API:${NC} https://localhost:8000/docs"
  echo -e "  ${BLUE}Database:${NC} localhost:5432"
  echo -e "${BLUE}================================================${NC}"
}

# Function to display logs
logs() {
  echo -e "${YELLOW}📋 Showing logs...${NC}"
  docker-compose logs -f
}

# Check command line arguments
case "$1" in
  build)
    check_docker
    clean_slate
    clean_build
    start "disable"
    ;;
  start)
    check_docker
    setup
    start "$2"
    ;;
  stop)
    check_docker
    stop
    ;;
  restart)
    check_docker
    stop
    start "$2"
    ;;
  logs)
    check_docker
    logs
    ;;
  *)
    echo -e "${BLUE}Usage:${NC} $0 {build|start|stop|restart|logs}"
    echo -e "  ${YELLOW}build${NC}    - Build all containers from scratch"
    echo -e "  ${YELLOW}start${NC}    - Start all services"
    echo -e "  ${YELLOW}stop${NC}     - Stop all services"
    echo -e "  ${YELLOW}restart${NC}  - Restart all services"
    echo -e "  ${YELLOW}logs${NC}     - Show container logs"
    exit 1
    ;;
esac

exit 0