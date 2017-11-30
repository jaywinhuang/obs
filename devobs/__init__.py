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
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('logs/obs.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('obs startup')

# Manage Logined user.
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# Database management
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from devobs import views, models
db.create_all()