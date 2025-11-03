from flask import Blueprint, jsonify
bp = Blueprint("foodref_bp", __name__)
@bp.get("/")
def stub():
    return jsonify({"status": "stub", "message": "FoodRef integration not implemented"}), 200
