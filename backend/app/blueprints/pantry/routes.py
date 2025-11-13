# === Pantry Routes (Smart CRUD) ===
from datetime import date, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...extensions import db
from ...models import PantryItem, SourceItem

bp = Blueprint("pantry_bp", __name__)

# --- helper ---
def _row(p: PantryItem):
    return {
        "id": p.id,
        "name": p.source_item.name if p.source_item else None,
        "quantity": p.quantity,
        "expiration_date": p.expiration_date.isoformat() if p.expiration_date else None,
    }

# --- list ---
@bp.get("/")
@jwt_required()
def list_pantry():
    uid = int(get_jwt_identity())
    rows = PantryItem.query.filter_by(user_id=uid).all()
    return jsonify([_row(p) for p in rows]), 200

# --- add (smart) ---
@bp.post("/")
@jwt_required()
def add_pantry():
    uid = int(get_jwt_identity())
    data = request.get_json() or {}
    name = data.get("name")
    qty = int(data.get("quantity", 1))
    exp = data.get("expiration_date")

    if not name:
        return jsonify({"error": "name required"}), 400

    # find or create source item
    si = SourceItem.query.filter_by(user_id=uid, name=name).first()
    if not si:
        si = SourceItem(user_id=uid, name=name)
        db.session.add(si)
        db.session.commit()

    expiration_date = None
    if exp:
        try:
            y, m, d = map(int, exp.split("-"))
            expiration_date = date(y, m, d)
        except Exception:
            expiration_date = None

    p = PantryItem(user_id=uid, source_item_id=si.id, quantity=qty, expiration_date=expiration_date)
    db.session.add(p)
    db.session.commit()
    return jsonify(_row(p)), 201

# --- update ---
@bp.patch("/<int:item_id>")
@jwt_required()
def update_pantry(item_id):
    uid = int(get_jwt_identity())
    data = request.get_json() or {}
    p = PantryItem.query.filter_by(id=item_id, user_id=uid).first()
    if not p:
        return jsonify({"error": "not found"}), 404

    if "quantity" in data:
        p.quantity = int(data["quantity"])
    if "expiration_date" in data:
        try:
            y, m, d = map(int, data["expiration_date"].split("-"))
            p.expiration_date = date(y, m, d)
        except Exception:
            p.expiration_date = None
    db.session.commit()
    return jsonify(_row(p)), 200

# --- delete ---
@bp.delete("/<int:item_id>")
@jwt_required()
def delete_pantry(item_id):
    uid = int(get_jwt_identity())
    p = PantryItem.query.filter_by(id=item_id, user_id=uid).first()
    if not p:
        return jsonify({"error": "not found"}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({"deleted": item_id}), 200

# --- expiring ---
@bp.get("/expiring")
@jwt_required()
def expiring():
    uid = int(get_jwt_identity())
    days = int(request.args.get("days", 7))
    cutoff = date.today() + timedelta(days=days)
    q = PantryItem.query.filter(
        PantryItem.user_id == uid,
        PantryItem.expiration_date.isnot(None),
        PantryItem.expiration_date <= cutoff,
    )
    return jsonify([_row(p) for p in q.all()]), 200
