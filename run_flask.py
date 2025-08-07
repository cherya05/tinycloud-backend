#!/usr/bin/env python3
import os
import sys
import subprocess

# Set environment variables
os.environ['FLASK_APP'] = 'tinycloud.app'
os.environ['PYTHONPATH'] = os.path.join(os.getcwd(), 'api')
os.environ['POSTGRES_USER'] = 'postgres'
os.environ['POSTGRES_PASSWORD'] = 'password'
os.environ['POSTGRES_DB'] = 'tinycloud'
os.environ['DATABASE_URL'] = 'postgresql://postgres:password@localhost:5432/tinycloud'

# Run the Flask command
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python run_flask.py <flask_command>")
        print("Example: python run_flask.py db init")
        sys.exit(1)
    
    # Change to the api directory
    api_dir = os.path.join(os.getcwd(), 'api')
    os.chdir(api_dir)
    
    # Run the Flask command
    cmd = ['flask'] + sys.argv[1:]
    subprocess.run(cmd) 