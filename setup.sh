#!/bin/bash

# Setup script for Streamlit Cloud deployment
# This script will be executed automatically by Streamlit Cloud

echo "Setting up CONSORCIO DEJ environment..."

# Check if we're on a system that supports apt-get
if command -v apt-get &> /dev/null; then
    echo "Installing system dependencies with apt-get..."
    apt-get update
    apt-get install -y fonts-liberation fontconfig
elif command -v yum &> /dev/null; then
    echo "Installing system dependencies with yum..."
    yum install -y liberation-fonts fontconfig
elif command -v brew &> /dev/null; then
    echo "Installing system dependencies with brew..."
    brew install fontconfig
else
    echo "No package manager found. Skipping system dependencies."
fi

echo "Setup completed successfully!" 