#!/bin/bash

# This script creates a virtual environment for a specific notebook
# Usage: create-notebook-venv.sh <notebook_path>

NOTEBOOK_PATH=$1
NOTEBOOK_DIR=$(dirname "$NOTEBOOK_PATH")
NOTEBOOK_NAME=$(basename "$NOTEBOOK_PATH" .ipynb)
VENV_PATH="${NOTEBOOK_DIR}/.venv_${NOTEBOOK_NAME}"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment for ${NOTEBOOK_NAME}..."
    python -m virtualenv "$VENV_PATH"
fi

# Activate the virtual environment and install dependencies
source "${VENV_PATH}/bin/activate"

# Look for requirements.txt in the notebook directory
if [ -f "${NOTEBOOK_DIR}/requirements.txt" ]; then
    echo "Installing requirements from ${NOTEBOOK_DIR}/requirements.txt..."
    pip install -r "${NOTEBOOK_DIR}/requirements.txt"
fi

# Parse pip install commands from the notebook and install them
if [ -f "$NOTEBOOK_PATH" ]; then
    echo "Installing dependencies from notebook..."
    DEPS=$(grep -A1 '"pip install' "$NOTEBOOK_PATH" | grep -v '"pip install' | tr -d '"' | tr -d ',')
    if [ ! -z "$DEPS" ]; then
        pip install $DEPS
    fi
fi

echo "Virtual environment ready at: $VENV_PATH" 