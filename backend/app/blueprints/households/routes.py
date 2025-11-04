# app/blueprints/households/routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...extensions import db
from ...models import Household, User

bp = Blueprint("households", __name__)

# === GET all households ===
@bp.get("/")
@jwt_required()
def get_households():
    households = Household.query.all()
    return jsonify([
        {"id": h.id, "name": h.name, "created_at": h.created_at.isoformat()} for h in households
    ]), 200

# === POST create household ===
@bp.post("/")
@jwt_required()
def create_household():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "Household name required"}), 400
    if Household.query.filter_by(name=name).first():
        return jsonify({"error": "Household already exists"}), 400
    new_hh = Household(name=name)
    db.session.add(new_hh)
    db.session.commit()
    return jsonify({"id": new_hh.id, "name": new_hh.name}), 201

# === PATCH rename household ===
@bp.patch("/<int:household_id>")
@jwt_required()
def rename_household(household_id):
    hh = Household.query.get_or_404(household_id)
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "New name required"}), 400
    hh.name = name
    db.session.commit()
    return jsonify({"id": hh.id, "name": hh.name}), 200

# === DELETE household ===
@bp.delete("/<int:household_id>")
@jwt_required()
def delete_household(household_id):
    hh = Household.query.get_or_404(household_id)
    db.session.delete(hh)
    db.session.commit()
    return jsonify({"message": f"Household {household_id} deleted"}), 200

# === Optional: add user to household ===
@bp.post("/<int:household_id>/add_user")
@jwt_required()
def add_user_to_household(household_id):
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    hh = Household.query.get_or_404(household_id)
    user.household_id = hh.id
    db.session.commit()
    return jsonify({"message": f"User {user.id} added to household {hh.name}"}), 200
