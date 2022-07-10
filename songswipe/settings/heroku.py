"""
Production Settings for Heroku
"""

import os 
from pathlib import Path

# From environ package
import environ

from .dev import *

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(Path(BASE_DIR, '.env'))

# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.db(),
}