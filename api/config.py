import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
    "mysql+pymysql://dev:devpass@localhost:3306/quizdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False