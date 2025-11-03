from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...extensions import db
from ...models import GroceryList, GroceryListItem, SourceItem

bp = Blueprint("lists_bp", __name__)

def _get_active_list(uid: int) -> GroceryList:
    gl = GroceryList.query.filter_by(user_id=uid, is_active=True).first()
    if not gl:
        gl = GroceryList(user_id=uid, name="My List", is_active=True)
        db.session.add(gl); db.session.commit()
    return gl

def _list_row(gl: GroceryList):
    items = GroceryListItem.query.filter_by(list_id=gl.id).all()
    return {"id": gl.id, "name": gl.name, "is_active": gl.is_active,
            "items": [{"id": i.id, "source_item_id": i.source_item_id, "quantity": i.quantity, "checked": i.checked} for i in items]}

@bp.get("/active")
@jwt_required()
def get_active():
    uid = int(get_jwt_identity())
    gl = _get_active_list(uid)
    return jsonify(_list_row(gl)), 200

@bp.post("/active/add")
@jwt_required()
def add_to_active():
    uid = int(get_jwt_identity())
    data = request.get_json() or {}
    source_item_id = data.get("source_item_id")
    quantity = int(data.get("quantity", 1))
    if not source_item_id:
        return jsonify({"error": "source_item_id required"}), 400
    si = SourceItem.query.filter_by(id=source_item_id, user_id=uid).first()
    if not si:
        return jsonify({"error": "invalid source_item_id"}), 400
    gl = _get_active_list(uid)
    gli = GroceryListItem(list_id=gl.id, source_item_id=source_item_id, quantity=quantity, checked=False)
    db.session.add(gli); db.session.commit()
    return jsonify(_list_row(gl)), 201

@bp.post("/active/check")
@jwt_required()
def check_item():
    uid = int(get_jwt_identity())
    data = request.get_json() or {}
    item_id = data.get("item_id")
    checked = bool(data.get("checked", True))
    gl = _get_active_list(uid)
    gli = GroceryListItem.query.join(GroceryList).filter(
        GroceryList.id == gl.id, GroceryListItem.id == item_id).first()
    if not gli:
        return jsonify({"error": "not found"}), 404
    gli.checked = checked; db.session.commit()
    return jsonify(_list_row(gl)), 200

@bp.post("/active/archive")
@jwt_required()
def archive_active():
    uid = int(get_jwt_identity())
    gl = _get_active_list(uid)
    gl.is_active = False; db.session.commit()
    _get_active_list(uid)
    return jsonify({"status": "archived"}), 200
