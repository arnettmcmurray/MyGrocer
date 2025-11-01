from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User

users_bp = Blueprint("users", __name__)

@users_bp.get("/me")
@jwt_required()
def me():
    uid = get_jwt_identity()
    u = User.query.get_or_404(uid)
    return jsonify({"id": u.id, "email": u.email, "name": u.name, "created_at": u.created_at.isoformat()})
