#!/bin/bash
# Linux-optimized Azure App Service startup script
set -e  # Exit immediately if a command exits with non-zero status

# Function for error logging
log_error() {
    echo "ERROR: $1" >&2
    exit 1
}

# Function for info logging
log_info() {
    echo "INFO: $1"
}

# Base directory for the application
APP_DIR="/home/site/wwwroot"
log_info "Application directory: $APP_DIR"

# Set production environment for Azure
export DJANGO_ENV="prod"
log_info "DJANGO_ENV set to: $DJANGO_ENV"

# Ensure we're in the correct directory
cd "$APP_DIR" || log_error "Failed to change to app directory: $APP_DIR"

# Detect Python and set command
if command -v python3 &> /dev/null; then
    log_info "Python 3 found: $(python3 --version)"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    log_info "Python found: $(python --version)"
    PYTHON_CMD="python"
else
    log_error "Python not found. Check your environment configuration."
fi

# Set appropriate PYTHONPATH for Linux environment
export PYTHONPATH="$APP_DIR:$PYTHONPATH"
log_info "PYTHONPATH set to: $PYTHONPATH"

# Set Django settings module
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-"core.settings.prod"}
log_info "DJANGO_SETTINGS_MODULE set to: $DJANGO_SETTINGS_MODULE"

# Install dependencies with error handling
log_info "Installing dependencies..."
pip install -r "$APP_DIR/requirements.txt" || log_error "Failed to install dependencies."

# Run database migrations
log_info "Applying database migrations..."
$PYTHON_CMD manage.py migrate --noinput || log_error "Failed to apply migrations."

# Collect static files
log_info "Collecting static files..."
$PYTHON_CMD manage.py collectstatic --noinput --clear || log_error "Failed to collect static files."

# Start Gunicorn for production with appropriate Linux settings
log_info "Starting Gunicorn server..."
if ! command -v gunicorn &> /dev/null; then
    log_info "Gunicorn not found, installing..."
    pip install gunicorn || log_error "Failed to install Gunicorn."
fi

# Export port for Azure Linux App Service
export PORT=${PORT:-8000}
log_info "Using port: $PORT"

# Execute Gunicorn with optimized settings for Linux App Service
exec gunicorn core.wsgi:application \
    --bind=0.0.0.0:$PORT \
    --workers=${GUNICORN_WORKERS:-3} \
    --timeout=${GUNICORN_TIMEOUT:-120} \
    --access-logfile='-' \
    --error-logfile='-'