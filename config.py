# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "mysql://obs_dev:obs_dev_admin@jaydbinstance.cshar3yujlmy.us-east-1.rds.amazonaws.com:3306/obs"
# SQLALCHEMY_DATABASE_URI = "mysql://localhost:3306/obs"
SQLALCHEMY_TRACK_MODIFICATIONS = True

# email config
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ''
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False

# available languages
LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}
