import os
basedir = os.path.abspath(os.path.dirname(__file__))

class LocalDevelopmentConfig():
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.sqlite3")
    UPLOAD_FOLDER = os.path.join(os.getcwd(),"static/upload_folder")
    DEBUG = True
    SECRET_KEY =  "ash ah secet"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "really super secret" # Read from ENV in your case
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None

