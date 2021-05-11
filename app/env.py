import os

APP_ENV = os.environ.get("APP_ENV", "development")

ELASTICSEARCH = {
    'HOST': os.environ.get("ELS_HOST", None),
    'USER': os.environ.get("ELS_USERNAME", None),
    'PASSWORD': os.environ.get("ELS_PASSWORD", None),
    'TEXT_INDEX': os.environ.get("ELS_TEXT_INDEX", None)
}

SUPPORT = os.environ.get("SUPPORT", 0.015)
