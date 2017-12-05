# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "mysql://obs_dev:obs_dev_admin@jaydbinstance.cshar3yujlmy.us-east-1.rds.amazonaws.com:3306/obs"
SQLALCHEMY_TRACK_MODIFICATIONS = True


# available languages
LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}

