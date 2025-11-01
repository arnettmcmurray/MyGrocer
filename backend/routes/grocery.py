from collections import defaultdict
from datetime import date
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.extensions import db
from backend.models import List, Item, PlanEntry, list_items

grocery_bp = Blueprint("grocery", __name__)

def _user_list(uid: int, name: str) -> List:
    lst = List.query.filter_by(user_id=uid, name=name).first()
    if not lst:
        lst = List(user_id=uid, name=name)
        db.session.add(lst); db.session.flush()
    return lst

@grocery_bp.post("/from-plan")
@jwt_required()
def build_from_plan():
    uid = get_jwt_identity()
    data = request.get_json() or {}
    start = data.get("from"); end = data.get("to")
    if not start or not end:
        return jsonify({"error": "from and to required (YYYY-MM-DD)"}), 400
    start_d = date.fromisoformat(start); end_d = date.fromisoformat(end)

    plans = PlanEntry.query.filter_by(user_id=uid).filter(PlanEntry.day >= start_d, PlanEntry.day <= end_d).all()

    need = defaultdict(int)
    for p in plans:
        for ing in p.recipe.ingredients_json or []:
            need[ing["name"].lower()] += ing.get("qty", 1)

    have = defaultdict(int)
    user_items = Item.query.join(list_items).join(List).filter(List.user_id == uid).all()
    for it in user_items:
        have[it.name.lower()] += max(0, it.quantity - it.reserved_qty)

    missing = defaultdict(int)
    for nm, qty in need.items():
        diff = qty - have.get(nm, 0)
        if diff > 0:
            missing[nm] += diff

    grocery = _user_list(uid, "Grocery")
    grocery.items.clear(); db.session.flush()

    for nm, qty in missing.items():
        item = Item(name=nm, quantity=qty)
        db.session.add(item); db.session.flush()
        grocery.items.append(item)

    db.session.commit()
    return jsonify({"message": "Grocery list built", "missing_count": len(missing)}), 201
