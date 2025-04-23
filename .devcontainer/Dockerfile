FROM mcr.microsoft.com/devcontainers/python:3.12

# Install PostgreSQL client
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends postgresql-client \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Install additional Python tools
RUN pip install --upgrade pip \
    && pip install pytest django-debug-toolbar