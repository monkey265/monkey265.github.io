#!/bin/bash
# Move to the script directory
cd "$(dirname "$0")"

# Use the virtual environment Python if available, otherwise global
if [ -f "./venv/bin/python3" ]; then
    PYTHON_EXEC="./venv/bin/python3"
else
    PYTHON_EXEC="python3"
fi

echo "Using Python: $PYTHON_EXEC"
$PYTHON_EXEC update_prices.py
