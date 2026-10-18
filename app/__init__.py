# __init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config, TestConfig
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create SQLAlchemy instance
db = SQLAlchemy()

# Create Flask-Migrate instance
migrate = Migrate()

if os.getenv('APP_ENVIRONMENT') == "testing":
    config = TestConfig
else:
    config = Config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
migrate.init_app(app, db)


from app import models, views
