import os

class Config:
    SECRET_KEY = os.urandom(24)  # For session management
    SQLALCHEMY_DATABASE_URI = 'sqlite:///student_info_system.db'  # SQLite database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
