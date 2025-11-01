from flask import Blueprint, jsonify
health_bp = Blueprint("health", __name__)

@health_bp.get("/")
def root():
    return jsonify({"message": "MyGrocer API is live"})

@health_bp.get("/health")
def health():
    return jsonify({"status": "ok"})
