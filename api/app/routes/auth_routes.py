from flask import Blueprint, request, jsonify
from ..models import User
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth_api', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    # Hash the password before storing
    hashed_password = generate_password_hash(password)
    # TODO: Hash password in production
    user = User(username=username, password=hashed_password) 
    db.session.add(user)
    db.session.commit()

    return jsonify({'id': user.id, 'username': user.username}), 201
# Login route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return jsonify({"id": user.id, "username": user.username}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401