#!/usr/bin/env bash

# Function to start Docker Desktop
start_docker_desktop() {
    open -a Docker
}

# Function to check if Docker is running
is_docker_running() {
    docker info > /dev/null 2>&1
    return $?
}

# Function to ensure Docker is running
ensure_docker_is_running() {
    if is_docker_running; then
        echo "Docker is already running"
    else
        echo "Docker is not running. Attempting to start Docker Desktop..."
        start_docker_desktop

        while ! is_docker_running; do
            echo "Waiting for Docker to start..."
            sleep 2
        done
        
        echo "Docker started successfully."
    fi
}

case ${1} in
start-docker)
	ensure_docker_is_running
;;
build)
  cd ..
  docker build -t wealth-planner:latest .
  echo "new wealth-planner:latest image built."
;;
start)
	ensure_docker_is_running
	echo "Starting Wealth Planner"
	cd ../docker
	docker-compose -f docker-compose.yml up -d
;;
stop)
    echo "Starting the postgres database"
    cd ../docker
    docker-compose down
;;
esac