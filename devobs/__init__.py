import os
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from logging.handlers import RotatingFileHandler
import logging

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object('config')

# Logging
handler = RotatingFileHandler('obs.log', maxBytes=1024*1024, backupCount=20)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from devobs import views, models

db.create_all()