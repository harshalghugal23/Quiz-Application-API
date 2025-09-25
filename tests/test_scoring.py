import pytest
from app import create_app, db
from app.services.quiz_service import QuizService

@pytest.fixture
def app():
    app = create_app()
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture
def client(app):
    return app.test_client()


def test_scoring_single_and_multiple(app):
    # create quiz
    q = QuizService.create_quiz('Sample')
    # add single
    q1 = QuizService.add_question(q.id, '1+1?', 'single', options=[
        {'text': '1', 'is_correct': False},
        {'text': '2', 'is_correct': True}
    ])
    # add multiple
    q2 = QuizService.add_question(q.id, 'Select primes', 'multiple', options=[
        {'text': '2', 'is_correct': True},
        {'text': '3', 'is_correct': True},
        {'text': '4', 'is_correct': False}
    ])
    # submit answers
    res = QuizService.evaluate_submission(q.id, [
        {'question_id': q1.id, 'selected_option_ids': [q1.options[1].id]},
        {'question_id': q2.id, 'selected_option_ids': [q2.options[0].id, q2.options[1].id]}
    ])
    assert res['score'] == 2
    assert res['total'] == 2


def test_text_question_word_limit(app):
    q = QuizService.create_quiz('TextQuiz')
    qt = QuizService.add_question(q.id, 'Write a short note', 'text', options=None, max_words=5)
    # within limit
    res_ok = QuizService.evaluate_submission(q.id, [
        {'question_id': qt.id, 'text_answer': 'one two three'}
    ])
    assert res_ok['score'] == 1
    # over limit
    res_bad = QuizService.evaluate_submission(q.id, [
        {'question_id': qt.id, 'text_answer': 'one two three four five six'}
    ])
    assert res_bad['score'] == 0