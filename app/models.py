from . import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    questions = relationship('Question', backref='quiz', cascade='all, delete-orphan')


class Question(db.Model):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    text = Column(Text, nullable=False)
    type = Column(String(50), nullable=False) # 'single', 'multiple', 'text'
    max_words = Column(Integer, nullable=True) # used for text typed answers
    options = relationship('Option', backref='question', cascade='all, delete-orphan')


class Option(db.Model):
    __tablename__ = 'options'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    text = Column(String(500), nullable=False)
    is_correct = Column(Boolean, default=False)