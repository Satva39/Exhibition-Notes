import os

import cloudinary

cloudinary.config(
    cloud_name="olrnljeq",
    api_key="131355548499872",
    api_secret="dsEl-2FNZe2fR3du8TRIlXtTmSM",
    secure=True
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "ExpoNoteCRMSecret2026"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "uploads"
    )

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024