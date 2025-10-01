# app/admin.py
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import Quiz, Question, Option
from . import db

def setup_admin(app):
    admin = Admin(app, name='Quiz Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(Quiz, db.session))
    admin.add_view(ModelView(Question, db.session))
    admin.add_view(ModelView(Option, db.session))
