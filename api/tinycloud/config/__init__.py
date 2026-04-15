import os

class Config:
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    hostname = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{user}:{password}@{hostname}:{port}/{name}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
