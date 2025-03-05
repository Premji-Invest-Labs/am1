#!/bin/bash

# Stop on errors
set -e

echo "Setting up your development environment..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

### Detecting the OS type
OS_TYPE=$(uname -s)

# macOS Setup
if [[ "$OS_TYPE" == "Darwin" ]]; then
    echo "macOS detected"

    # Step 1: Install Docker if not installed
    if ! command_exists docker; then
        echo "Docker not found. Installing Docker..."
        # Install Docker using Homebrew (ensure Homebrew is installed)
        if ! command_exists brew; then
            echo "Homebrew not found. Please install Homebrew first: https://brew.sh/"
            exit 1
        fi
        brew install --cask docker
        echo "Docker installed successfully!"
    else
        echo "Docker is already installed."
    fi

    # Step 2: Ensure Docker is running
    open -a Docker || sudo systemctl start docker

# Linux Setup (Ubuntu)
elif [[ "$OS_TYPE" == "Linux" ]]; then
    echo "Linux (Ubuntu) detected"

    # Step 1: Install Docker if not installed
    if ! command_exists docker; then
        echo "Docker not found. Installing Docker..."
        sudo apt update
        sudo apt install -y docker.io
        echo "Docker installed successfully!"
    else
        echo "Docker is already installed."
    fi

    # Step 2: Ensure Docker is running
    sudo systemctl start docker || echo "Docker is already running"

# Windows Setup
elif [[ "$OS_TYPE" == "CYGWIN"* || "$OS_TYPE" == "MINGW"* ]]; then
    echo "Windows detected"

    # Check if Docker Desktop is installed
    if ! command_exists docker; then
        echo "Docker not found. Please download Docker Desktop for Windows from https://www.docker.com/products/docker-desktop"
        exit 1
    else
        echo "Docker is already installed."
    fi

    # Check if Docker is running (Windows specific)
    docker version > /dev/null 2>&1 || echo "Docker is not running. Please open Docker Desktop manually."

else
    echo "Unsupported OS. This script supports macOS, Linux (Ubuntu), and Windows."
    exit 1
fi

# Step 3: Ask User for AI Model Choice
echo ""
echo "Choose AI Model Setup:"
echo "1) OpenAI API Key [Keep your API Key handy]"
echo "2) Download and Run Ollama (LLaMA Model) locally [Make sure you have GPU and sufficient RAM]"
read -p "Enter 1 or 2: " ai_choice

if [[ "$ai_choice" == "1" ]]; then
    read -p "Enter your OpenAI API Key: " OPENAI_API_KEY
    echo "OpenAI API Key set!"
    export OPENAI_API_KEY
elif [[ "$ai_choice" == "2" ]]; then
    echo "Downloading and setting up Ollama..."

    # Install Ollama (LLaMA Model) if not installed
    if ! command_exists ollama; then
        echo "Installing Ollama..."
        if [[ "$OS_TYPE" == "Darwin" ]]; then
            # macOS
            curl -fsSL https://ollama.ai/install.sh | sh
        elif [[ "$OS_TYPE" == "Linux" ]]; then
            # Linux (Ubuntu)
            curl -fsSL https://ollama.ai/install.sh | sh
        else
            echo "Ollama installation not supported for your OS. Please check Ollama's documentation for Windows setup."
            exit 1
        fi
    fi

    echo "Downloading LLaMA3.2-vision:11b-instruct-q4_K_M model..."
    ollama pull llama3.2-vision:11b-instruct-q4_K_M

    echo "LLaMA model is ready!"
else
    echo "Invalid choice! Exiting..."
    exit 1
fi

echo "Setup complete!"
echo "Execute 'run_dockerized.sh' to start the application."