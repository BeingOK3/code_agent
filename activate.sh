#!/bin/bash
# Quick activation script for uv virtual environment

cd "$(dirname "$0")" || exit 1

if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✓ Virtual environment activated"
    echo "✓ Python: $(python3 --version)"
    echo "✓ Ready to run: python3 main.py"
else
    echo "✗ Virtual environment not found. Run 'uv venv' first."
    exit 1
fi
