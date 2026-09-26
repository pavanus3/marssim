#!/bin/bash
set -e

echo "=== Setting up marssim and ADRS environment for Google Cloud (Debian/Ubuntu) ==="

# Update package lists
sudo apt-get update -y

# Install system dependencies (C++ build tools, CMake, Protobuf for marssim)
sudo apt-get install -y build-essential cmake libprotobuf-dev protobuf-compiler git python3-pip python3-venv

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

echo "=== Setup Complete for GCP ==="
echo "To activate the environment, run: source adrs_env/bin/activate"
