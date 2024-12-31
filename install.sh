#!/bin/bash

# Install Python dependencies
pip install -e .

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "Google Cloud SDK not found. Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if GOOGLE_APPLICATION_CREDENTIALS is set
if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set"
    echo "Please set it to point to your Google Cloud credentials JSON file:"
    echo "export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json"
fi

# Enable Text-to-Speech API if not already enabled
echo "Note: Make sure the Cloud Text-to-Speech API is enabled in your Google Cloud Console"
echo "Visit: https://console.cloud.google.com/apis/library/texttospeech.googleapis.com"

# Make the script executable
chmod +x install.sh 