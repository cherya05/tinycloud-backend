from api.tinycloud import models
from api.tinycloud import create_app

app = create_app()

@app.cli.command('migrate')
def migrate():
    from api.tinycloud import db
    db.create_all()

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
        from api.tinycloud import db
        db.drop_all()
        print("Database wiped successfully.")
    else:
        print("This command can only be run in debug mode.")

@app.cli.command('create')
def create():
    """Create all tables in the database."""
    from api.tinycloud import db
    db.create_all()
    print("Database created successfully.")