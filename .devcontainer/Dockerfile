FROM mcr.microsoft.com/devcontainers/python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install base Jupyter and ipykernel
RUN pip install --no-cache-dir \
    jupyter \
    ipykernel \
    virtualenv

# Create workspace directory
WORKDIR /workspace

# Add script to create per-notebook venvs
COPY create-notebook-venv.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/create-notebook-venv.sh

# Set up command history
RUN echo "export HISTFILE=/workspace/.bash_history" >> ~/.bashrc 