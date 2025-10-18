#!/bin/bash

# Source .env file but don't override existing environment variables
if [ -f .env ]; then
    # Read .env file and only set variables that aren't already set
    while IFS= read -r line; do
        # Skip comments and empty lines
        [[ $line =~ ^[[:space:]]*# ]] && continue
        [[ -z "${line// }" ]] && continue
        
        # Extract variable name
        var_name=$(echo "$line" | cut -d'=' -f1)
        
        # Only set if not already defined
        if [ -z "${!var_name}" ]; then
            export "$line"
        fi
    done < .env
fi

export FLASK_APP=manage.py

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Check if migrations directory exists and has migration files
if [ ! -d "migrations/versions" ] || [ -z "$(ls -A migrations/versions 2>/dev/null | grep -v __pycache__)" ]; then
    echo "No migrations found. Initializing database..."
    
    # Initialize migrations if not already done
    if [ ! -f "migrations/alembic.ini" ]; then
        echo "Initializing Flask-Migrate..."
        flask db init
    fi
    
    # Create initial migration
    echo "Creating initial migration..."
    flask db migrate -m "Create url table"
fi

# Apply any pending migrations
echo "Applying database migrations..."
flask db upgrade

# Start the Flask application
echo "Starting Flask application..."
gunicorn --bind 0.0.0.0:8081 --workers 1 manage:app