from flask import request, jsonify
from ..schemas import QuizCreateSchema, QuestionCreateSchema, SubmitAnswersSchema
from ..services.quiz_service import QuizService
from .. import db
from marshmallow import ValidationError

class QuizController:

    @staticmethod
    def create_quiz():
        try:
            data = QuizCreateSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400

        quiz = QuizService.create_quiz(data['title'])
        return jsonify({'id': quiz.id, 'title': quiz.title}), 201

    @staticmethod
    def add_question(quiz_id):
        try:
            data = QuestionCreateSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400

        try:
            q = QuizService.add_question(
                quiz_id=quiz_id,
                text=data['text'],
                qtype=data['type'],
                options=data.get('options'),
                max_words=data.get('max_words')
            )
        except ValueError as e:
            return jsonify({'error': str(e)}), 404

        return jsonify({'id': q.id, 'text': q.text, 'type': q.type}), 201

    @staticmethod
    def get_questions(quiz_id):
        out = QuizService.get_quiz_questions_for_taking(quiz_id)
        if out is None:
            return jsonify({'error': 'Quiz not found'}), 404
        return jsonify({'questions': out}), 200

    @staticmethod
    def submit_answers(quiz_id):
        try:
            data = SubmitAnswersSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400

        try:
            res = QuizService.evaluate_submission(quiz_id, data['answers'])
        except ValueError as e:
            return jsonify({'error': str(e)}), 404

        return jsonify(res), 200

    @staticmethod
    def list_quizzes():
        return jsonify({'quizzes': QuizService.list_quizzes()}), 200

