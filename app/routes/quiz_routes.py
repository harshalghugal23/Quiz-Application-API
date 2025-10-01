from flask import Blueprint, request
from ..controllers.quiz_controller import QuizController

quiz_bp = Blueprint('quiz_api', __name__)  # remove strict_slashes

# Quiz management
@quiz_bp.route('/', methods=['POST'])
@quiz_bp.route('', methods=['POST'])  # allows /api as well
def create_quiz():
    return QuizController.create_quiz()

@quiz_bp.route('/', methods=['GET'])
@quiz_bp.route('', methods=['GET'])
def list_quizzes():
    return QuizController.list_quizzes()

# Questions
@quiz_bp.route('/<int:quiz_id>/questions', methods=['POST'])
def add_question(quiz_id):
    return QuizController.add_question(quiz_id)

@quiz_bp.route('/<int:quiz_id>/questions', methods=['GET'])
def get_questions(quiz_id):
    return QuizController.get_questions(quiz_id)

# Submit answers
@quiz_bp.route('/<int:quiz_id>/submit', methods=['POST'])
def submit_answers(quiz_id):
    return QuizController.submit_answers(quiz_id)
