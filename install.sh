#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting installation...${NC}"

# Check if Python 3.10 or higher is installed
if ! command -v python3.10 &> /dev/null; then
    echo -e "${RED}Python 3.10 or higher is required but not installed.${NC}"
    echo -e "${YELLOW}Please install Python 3.10 or higher and try again.${NC}"
    exit 1
fi

# Create and activate virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3.10 -m venv .venv
source .venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
python -m pip install --upgrade pip

# Install PyAudio system dependencies if not already installed
if ! dpkg -l | grep -q "libportaudio2"; then
    echo -e "${YELLOW}Installing PyAudio system dependencies...${NC}"
    sudo apt-get update
    sudo apt-get install -y portaudio19-dev python3-pyaudio
fi

# Check if CUDA is available
if command -v nvidia-smi &> /dev/null; then
    echo -e "${GREEN}CUDA detected - Installing with CUDA support${NC}"
    pip install -e ".[cuda]"
else
    echo -e "${YELLOW}CUDA not detected - Installing CPU version${NC}"
    pip install -e ".[cpu]"
fi

echo -e "${GREEN}Installation complete!${NC}"
echo -e "${YELLOW}To activate the virtual environment, run:${NC}"
echo -e "${GREEN}source .venv/bin/activate${NC}" 