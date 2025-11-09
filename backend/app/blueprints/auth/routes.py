from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from ...extensions import db
from ...models import User

bp = Blueprint("auth", __name__)

@bp.post("/register")
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "email and password required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already registered"}), 409
    u = User(email=email); u.set_password(password)
    db.session.add(u); db.session.commit()
    return jsonify({"id": u.id, "email": u.email}), 201

@bp.post("/login")
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    u = User.query.filter_by(email=email).first()
    if not u or not u.check_password(password):
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({
        "access_token": create_access_token(identity=str(u.id)),
        "refresh_token": create_refresh_token(identity=str(u.id))
    }), 200

@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()           # this is already a string
    return jsonify({"access_token": create_access_token(identity=user_id)}), 200
