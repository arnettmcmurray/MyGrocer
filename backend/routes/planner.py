from datetime import date
from collections import defaultdict
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.extensions import db
from backend.models import PlanEntry, Recipe, Item, List, list_items

planner_bp = Blueprint("planner", __name__)

def _reserve_for_recipe(uid: int, recipe: Recipe):
    need = defaultdict(int)
    for ing in recipe.ingredients_json or []:
        need[ing["name"].lower()] += ing.get("qty", 1)
    inv = Item.query.join(list_items).join(List).filter(List.user_id == uid).all()
    for it in inv:
        nm = it.name.lower()
        if need.get(nm, 0) > 0:
            free = max(0, it.quantity - it.reserved_qty)
            if free > 0:
                take = min(free, need[nm])
                it.reserved_qty += take
                need[nm] -= take
    db.session.flush()

@planner_bp.post("")
@jwt_required()
def add_plan():
    uid = get_jwt_identity()
    data = request.get_json() or {}
    r_id = data.get("recipe_id"); day_str = data.get("day")
    if not r_id or not day_str:
        return jsonify({"error": "recipe_id and day required"}), 400
    r = Recipe.query.get_or_404(r_id)
    day = date.fromisoformat(day_str)
    entry = PlanEntry(user_id=uid, recipe_id=r.id, day=day)
    db.session.add(entry)
    _reserve_for_recipe(uid, r)
    db.session.commit()
    return jsonify({"id": entry.id, "recipe_id": r.id, "day": entry.day.isoformat()}), 201

@planner_bp.get("")
@jwt_required()
def list_plan():
    uid = get_jwt_identity()
    start = request.args.get("from")
    end = request.args.get("to")
    q = PlanEntry.query.filter_by(user_id=uid)
    if start:
        q = q.filter(PlanEntry.day >= date.fromisoformat(start))
    if end:
        q = q.filter(PlanEntry.day <= date.fromisoformat(end))
    rows = q.order_by(PlanEntry.day.asc()).all()
    return jsonify([{"id": e.id, "recipe_id": e.recipe_id, "title": e.recipe.title, "day": e.day.isoformat()} for e in rows])
