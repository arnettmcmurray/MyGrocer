from datetime import date, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...extensions import db
from ...models import PantryItem, SourceItem
bp = Blueprint("pantry_bp", __name__)
def _row(p: PantryItem):
    return {"id": p.id, "source_item_id": p.source_item_id, "quantity": p.quantity, "expiration_date": p.expiration_date.isoformat() if p.expiration_date else None}
@bp.get("/")
@jwt_required()
def list_pantry():
    uid = get_jwt_identity()
    rows = PantryItem.query.filter_by(user_id=uid).all()
    return jsonify([_row(p) for p in rows]), 200
@bp.post("/")
@jwt_required()
def add_pantry():
    uid = get_jwt_identity()
    data = request.get_json() or {}
    source_item_id = data.get("source_item_id")
    quantity = int(data.get("quantity", 1))
    exp = data.get("expiration_date")
    if not source_item_id:
        return jsonify({"error": "source_item_id required"}), 400
    si = SourceItem.query.filter_by(id=source_item_id, user_id=uid).first()
    if not si:
        return jsonify({"error": "invalid source_item_id"}), 400
    expiration_date = None
    if exp:
        try:
            y, m, d = map(int, exp.split("-"))
            expiration_date = date(y, m, d)
        except Exception:
            return jsonify({"error": "bad expiration_date"}), 400
    p = PantryItem(user_id=uid, source_item_id=source_item_id, quantity=quantity, expiration_date=expiration_date)
    db.session.add(p); db.session.commit()
    return jsonify(_row(p)), 201
@bp.get("/expiring")
@jwt_required()
def expiring():
    uid = get_jwt_identity()
    days = int(request.args.get("days", 7))
    cutoff = date.today() + timedelta(days=days)
    q = PantryItem.query.filter(PantryItem.user_id == uid, PantryItem.expiration_date.isnot(None), PantryItem.expiration_date <= cutoff)
    return jsonify([_row(p) for p in q.all()]), 200
