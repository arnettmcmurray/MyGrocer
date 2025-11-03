from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...extensions import db
from ...models import SourceItem, Category

bp = Blueprint("items_bp", __name__)

def _row(i: SourceItem):
    return {"id": i.id, "name": i.name, "category_id": i.category_id}

@bp.get("/")
@jwt_required()
def list_items():
    uid = int(get_jwt_identity())
    q = SourceItem.query.filter_by(user_id=uid)
    return jsonify([_row(i) for i in q.order_by(SourceItem.name.asc()).all()]), 200

@bp.post("/")
@jwt_required()
def create_item():
    uid = int(get_jwt_identity())
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    category_id = data.get("category_id")
    if not name:
        return jsonify({"error": "name required"}), 400
    if SourceItem.query.filter_by(user_id=uid, name=name).first():
        return jsonify({"error": "duplicate"}), 409
    if category_id:
        ok = Category.query.filter_by(id=category_id, user_id=uid).first()
        if not ok:
            return jsonify({"error": "invalid category"}), 400
    i = SourceItem(user_id=uid, name=name, category_id=category_id)
    db.session.add(i); db.session.commit()
    return jsonify(_row(i)), 201

@bp.put("/<int:item_id>")
@jwt_required()
def update_item(item_id: int):
    uid = int(get_jwt_identity())
    i = SourceItem.query.filter_by(id=item_id, user_id=uid).first()
    if not i:
        return jsonify({"error": "not found"}), 404
    data = request.get_json() or {}
    name = (data.get("name") or "").strip() or i.name
    category_id = data.get("category_id", i.category_id)
    if category_id:
        ok = Category.query.filter_by(id=category_id, user_id=uid).first()
        if not ok:
            return jsonify({"error": "invalid category"}), 400
    i.name = name; i.category_id = category_id
    db.session.commit()
    return jsonify(_row(i)), 200

@bp.delete("/<int:item_id>")
@jwt_required()
def delete_item(item_id: int):
    uid = int(get_jwt_identity())
    i = SourceItem.query.filter_by(id=item_id, user_id=uid).first()
    if not i:
        return jsonify({"error": "not found"}), 404
    db.session.delete(i); db.session.commit()
    return jsonify({"status": "deleted"}), 200
