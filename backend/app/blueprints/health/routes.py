from flask import Blueprint, jsonify
bp = Blueprint("health_bp", __name__)
@bp.get("/")
def ok():
    return jsonify({"status": "ok", "service": "mygrocer", "version": "mvp-1"}), 200
