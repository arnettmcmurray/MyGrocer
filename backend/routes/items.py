from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.extensions import db
from backend.models import Item, List, list_items

items_bp = Blueprint("items", __name__)

def _user_inventory_items(uid: int):
    q = Item.query.join(list_items).join(List).filter(List.user_id == uid).distinct()
    return q

@items_bp.get("")
@jwt_required()
def list_items():
    uid = get_jwt_identity()
    items = _user_inventory_items(uid).order_by(Item.created_at.desc()).all()
    return jsonify([{
        "id": i.id, "name": i.name, "quantity": i.quantity, "reserved_qty": i.reserved_qty,
        "category": i.category, "storage_area": i.storage_area,
        "expiration_date": i.expiration_date.isoformat() if i.expiration_date else None,
    } for i in items])

@items_bp.get("/expiring")
@jwt_required()
def list_expiring():
    from datetime import date, timedelta
    uid = get_jwt_identity()
    days = int(request.args.get("days", "7"))
    today = date.today(); cutoff = today + timedelta(days=days)
    items = _user_inventory_items(uid).filter(Item.expiration_date != None, Item.expiration_date <= cutoff).all()  # noqa: E711
    return jsonify([{
        "id": i.id, "name": i.name, "storage_area": i.storage_area,
        "expiration_date": i.expiration_date.isoformat() if i.expiration_date else None,
    } for i in items])
