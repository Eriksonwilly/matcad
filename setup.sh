#!/bin/bash

# Setup script for Streamlit Cloud deployment
# This script will be executed before the app starts

echo "Setting up environment for CONSORCIO DEJ..."

# Install system dependencies
apt-get update
apt-get install -y fonts-liberation fontconfig libgl1-mesa-glx libglib2.0-0

# Create necessary directories
mkdir -p .streamlit

# Set environment variables
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true

echo "Environment setup completed!" 