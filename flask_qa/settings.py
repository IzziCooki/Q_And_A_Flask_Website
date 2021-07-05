import os
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL?sslmode=require")
SECRET_KEY = os.environ.get("SECRET_KEY")
SQLALCHEMY_TRACK_MODIFICATION_ = False
