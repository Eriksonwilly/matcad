#!/bin/bash

# Setup script for Streamlit Cloud deployment
echo "Setting up CONSORCIO DEJ environment..."

# Install minimal system dependencies
apt-get update
apt-get install -y fonts-liberation fontconfig

echo "Setup completed!" 