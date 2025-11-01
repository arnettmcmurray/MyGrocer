from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from backend.extensions import db
from backend.models import User, List
from backend.utils import hash_password, verify_password

auth_bp = Blueprint("auth", __name__)
DEFAULT_LISTS = ["Pantry", "Fridge", "Freezer", "Grocery"]

@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    email = data.get("email"); password = data.get("password")
    if not email or not password:
        return jsonify({"error": "email and password required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already registered"}), 409

    user = User(email=email, password_hash=hash_password(password), name=data.get("name"))
    db.session.add(user); db.session.flush()
    for ln in DEFAULT_LISTS:
        db.session.add(List(name=ln, user_id=user.id))
    db.session.commit()
    return jsonify({"id": user.id, "email": user.email}), 201

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email"); password = data.get("password")
    if not email or not password:
        return jsonify({"error": "email and password required"}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(user.password_hash, password):
        return jsonify({"error": "invalid credentials"}), 401
    access = create_access_token(identity=user.id)
    refresh = create_refresh_token(identity=user.id)
    return jsonify({"access_token": access, "refresh_token": refresh})

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    uid = get_jwt_identity()
    access = create_access_token(identity=uid)
    return jsonify({"access_token": access})
