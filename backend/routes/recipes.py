from collections import defaultdict
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Recipe, Item, List, list_items

recipes_bp = Blueprint("recipes", __name__)

def _inventory_by_name(uid: int):
    q = Item.query.join(list_items).join(List).filter(List.user_id == uid).distinct()
    store = defaultdict(int)
    for i in q.all():
        store[i.name.lower()] += max(0, i.quantity - i.reserved_qty)
    return store

@recipes_bp.get("")
@jwt_required()
def list_recipes():
    uid = get_jwt_identity()
    time_max = request.args.get("time_max", type=int)
    difficulty = request.args.get("difficulty")
    no_shop = request.args.get("no_shop", default="false").lower() == "true"

    q = Recipe.query
    if time_max is not None:
        q = q.filter(Recipe.total_minutes <= time_max)
    if difficulty:
        q = q.filter(Recipe.difficulty == difficulty)

    have = _inventory_by_name(uid)
    out = []
    for r in q.all():
        ings = r.ingredients_json or []
        have_cnt = 0; need_cnt = 0
        missing = []
        for ing in ings:
            nm = ing["name"].lower()
            qty = ing.get("qty", 1)
            need_cnt += 1
            if have.get(nm, 0) >= qty:
                have_cnt += 1
            else:
                missing.append({"name": ing["name"], "qty": qty - have.get(nm, 0)})
        match = round(have_cnt / max(1, need_cnt), 2)
        if no_shop and missing:
            continue
        out.append({
            "id": r.id, "title": r.title, "minutes": r.total_minutes, "difficulty": r.difficulty,
            "match": match, "missing": missing, "ingredients": ings, "steps": r.steps_json.get("steps", []),
        })
    out.sort(key=lambda x: (-x["match"], x["minutes"]))
    return jsonify(out)
