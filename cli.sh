#!/bin/bash
# Code Agent Interactive CLI Launcher

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║     Code Agent - Interactive CLI       ║"
echo "║  Multi-Turn Conversation with Memory   ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies if needed
if ! python3 -c "import openai" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
fi

# Run the interactive CLI
echo -e "${GREEN}Starting interactive mode...${NC}\n"
python3 interactive_cli.py

echo -e "\n${GREEN}Thank you for using Code Agent!${NC}"
