from datetime import date
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.extensions import db
from backend.models import List, Item

lists_bp = Blueprint("lists", __name__)

@lists_bp.get("")
@jwt_required()
def list_lists():
    uid = get_jwt_identity()
    rows = List.query.filter_by(user_id=uid).all()
    return jsonify([{"id": l.id, "name": l.name, "user_id": l.user_id, "notes": l.notes} for l in rows])

@lists_bp.post("")
@jwt_required()
def create_list():
    uid = get_jwt_identity()
    data = request.get_json() or {}
    if "name" not in data:
        return jsonify({"error": "name required"}), 400
    lst = List(name=data["name"], user_id=uid, notes=data.get("notes"))
    db.session.add(lst); db.session.commit()
    return jsonify({"id": lst.id, "name": lst.name, "user_id": lst.user_id, "notes": lst.notes}), 201

@lists_bp.get("/<int:list_id>")
@jwt_required()
def get_list(list_id: int):
    uid = get_jwt_identity()
    l = List.query.filter_by(id=list_id, user_id=uid).first_or_404()
    items = [{
        "id": i.id, "name": i.name, "quantity": i.quantity, "reserved_qty": i.reserved_qty,
        "category": i.category, "storage_area": i.storage_area,
        "expiration_date": i.expiration_date.isoformat() if i.expiration_date else None,
    } for i in l.items]
    return jsonify({"id": l.id, "name": l.name, "user_id": l.user_id, "notes": l.notes, "items": items})

@lists_bp.post("/<int:list_id>/items")
@jwt_required()
def add_item_to_list(list_id: int):
    uid = get_jwt_identity()
    l = List.query.filter_by(id=list_id, user_id=uid).first_or_404()
    data = request.get_json() or {}

    if "item_id" in data:
        item = Item.query.get_or_404(data["item_id"])
    else:
        exp = data.get("expiration_date")
        exp_date = date.fromisoformat(exp) if isinstance(exp, str) and exp else None
        item = Item(
            name=data["name"],
            quantity=data.get("quantity", 1),
            category=data.get("category"),
            storage_area=data.get("storage_area"),
            upc=data.get("upc"),
            expiration_date=exp_date,
        )
        db.session.add(item); db.session.flush()

    if item not in l.items:
        l.items.append(item)
    db.session.commit()
    return jsonify({"message": "Item added", "list_id": l.id, "item_id": item.id}), 201

@lists_bp.delete("/<int:list_id>/items/<int:item_id>")
@jwt_required()
def remove_item_from_list(list_id: int, item_id: int):
    uid = get_jwt_identity()
    l = List.query.filter_by(id=list_id, user_id=uid).first_or_404()
    item = Item.query.get_or_404(item_id)
    if item in l.items:
        l.items.remove(item); db.session.commit()
    return jsonify({"message": "Item removed"})
