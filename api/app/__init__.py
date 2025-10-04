from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(config_class)

    db.init_app(app)

    from .routes.quiz_routes import quiz_bp
    app.register_blueprint(quiz_bp, url_prefix='/api/quizzes')
    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api')

    app.route('/')
    def home():
        return jsonify({"message": "Quiz API is running!"}), 200
    # create tables
    with app.app_context():
        db.create_all()


    return app