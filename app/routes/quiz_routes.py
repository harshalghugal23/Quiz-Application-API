from flask import Blueprint
from ..controllers.quiz_controller import QuizController

quiz_bp = Blueprint('quiz', __name__)

# Quiz management
quiz_bp.route('/quizzes', methods=['POST'])(QuizController.create_quiz)
quiz_bp.route('/quizzes', methods=['GET'])(QuizController.list_quizzes)

# Questions
quiz_bp.route('/quizzes/<int:quiz_id>/questions', methods=['POST'])(QuizController.add_question)
quiz_bp.route('/quizzes/<int:quiz_id>/questions', methods=['GET'])(QuizController.get_questions)

# Submit answers
quiz_bp.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])(QuizController.submit_answers)


