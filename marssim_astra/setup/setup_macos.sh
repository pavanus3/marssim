#!/bin/bash
set -e

echo "=== Setting up marssim and ADRS environment for macOS ==="

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Please install Homebrew first (https://brew.sh/)."
    exit 1
fi

# Install system dependencies (CMake, Protobuf for marssim)
brew install cmake protobuf git python@3.11

# Create Python virtual environment
python3 -m venv adrs_env
source adrs_env/bin/activate

# Install Python requirements
pip install --upgrade pip
pip install -r requirements.txt

# Clone required Git repositories
echo "Cloning marssim repository..."
git clone --recursive https://github.com/astra-sim/astra-sim.git || true

echo "Cloning UC Berkeley SkyDiscover repository..."
git clone https://github.com/skydiscover-ai/skydiscover.git || true

echo "Cloning UC Berkeley KISS Agent repository..."
git clone https://github.com/ksenxx/kiss_ai.git || true

echo "=== Setup Complete for macOS ==="
echo "To activate the environment, run: source adrs_env/bin/activate"
