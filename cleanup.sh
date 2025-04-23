#!/bin/bash
# Script to clean up redundant files in the project

# Create backup directory
BACKUP_DIR="./backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "Created backup directory: $BACKUP_DIR"

# Backup redundant files before deletion
echo "Backing up redundant files..."
cp -v app.py "$BACKUP_DIR/" 2>/dev/null || echo "No app.py found"
cp -v wsgi_app.py "$BACKUP_DIR/" 2>/dev/null || echo "No wsgi_app.py found"
cp -v startup.txt "$BACKUP_DIR/" 2>/dev/null || echo "No startup.txt found" 
cp -v startup.sh "$BACKUP_DIR/" 2>/dev/null || echo "No startup.sh found"
cp -v start.sh "$BACKUP_DIR/" 2>/dev/null || echo "No start.sh found"

# Remove redundant files now that we've backed them up
echo "Removing redundant files..."
rm -fv app.py wsgi_app.py startup.txt startup.sh start.sh

# Clean up __pycache__ directories
echo "Cleaning up __pycache__ directories..."
find . -name "__pycache__" -type d -exec rm -rf {} +

# Remove Scripts_Database if it exists (now moved to docs/database)
if [ -d "./Scripts_Database" ]; then
  echo "Removing Scripts_Database (already moved to docs/database)..."
  rm -rf ./Scripts_Database
fi

echo "Cleanup complete. Redundant files have been backed up to $BACKUP_DIR"