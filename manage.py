import os
from dotenv import load_dotenv
load_dotenv()

from api.tinycloud import models
import api.tinycloud.app
import api.tinycloud.extensions

app = api.tinycloud.app.create_app()

@app.cli.command('migrate')
def migrate():
    api.tinycloud.extensions.db.create_all()

@app.cli.command('routes')
def routes():
    print("Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

@app.cli.command('drop')
def drop():
    """Drop all tables in the database."""
    if app.debug:  # Only allow in debug mode for safety
        print("Dropping all tables...")
        api.tinycloud.extensions.db.drop_all()
        print("Database wiped successfully.")
    else:
        print("This command can only be run in debug mode.")

@app.cli.command('create')
def create():
    """Create all tables in the database."""
    api.tinycloud.extensions.db.create_all()
    print("Database created successfully.")