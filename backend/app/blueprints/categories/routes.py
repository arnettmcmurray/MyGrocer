from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...extensions import db
from ...models import Category
bp = Blueprint("categories_bp", __name__)
@bp.get("/")
@jwt_required()
def list_categories():
    uid = get_jwt_identity()
    rows = Category.query.filter_by(user_id=uid).order_by(Category.name.asc()).all()
    return jsonify([{"id": c.id, "name": c.name} for c in rows]), 200
@bp.post("/")
@jwt_required()
def create_category():
    uid = get_jwt_identity()
    name = (request.get_json() or {}).get("name", "").strip()
    if not name:
        return jsonify({"error": "name required"}), 400
    if Category.query.filter_by(user_id=uid, name=name).first():
        return jsonify({"error": "duplicate"}), 409
    c = Category(user_id=uid, name=name)
    db.session.add(c); db.session.commit()
    return jsonify({"id": c.id, "name": c.name}), 201
@bp.put("/<int:cat_id>")
@jwt_required()
def update_category(cat_id: int):
    uid = get_jwt_identity()
    c = Category.query.filter_by(id=cat_id, user_id=uid).first()
    if not c:
        return jsonify({"error": "not found"}), 404
    name = (request.get_json() or {}).get("name", "").strip()
    if not name:
        return jsonify({"error": "name required"}), 400
    c.name = name; db.session.commit()
    return jsonify({"id": c.id, "name": c.name}), 200
@bp.delete("/<int:cat_id>")
@jwt_required()
def delete_category(cat_id: int):
    uid = get_jwt_identity()
    c = Category.query.filter_by(id=cat_id, user_id=uid).first()
    if not c:
        return jsonify({"error": "not found"}), 404
    db.session.delete(c); db.session.commit()
    return jsonify({"status": "deleted"}), 200
