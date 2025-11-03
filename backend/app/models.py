from datetime import datetime
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    categories = db.relationship("Category", backref="user", lazy=True, cascade="all, delete-orphan")
    source_items = db.relationship("SourceItem", backref="user", lazy=True, cascade="all, delete-orphan")
    pantry_items = db.relationship("PantryItem", backref="user", lazy=True, cascade="all, delete-orphan")
    grocery_lists = db.relationship("GroceryList", backref="user", lazy=True, cascade="all, delete-orphan")
    def set_password(self, raw: str) -> None:
        self.password_hash = generate_password_hash(raw)
    def check_password(self, raw: str) -> bool:
        return check_password_hash(self.password_hash, raw)
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    __table_args__ = (db.UniqueConstraint("user_id", "name", name="uq_category_user_name"),)
class SourceItem(db.Model):
    __tablename__ = "source_items"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    category = db.relationship("Category", backref=db.backref("items", lazy=True))
    __table_args__ = (db.UniqueConstraint("user_id", "name", name="uq_sourceitem_user_name"),)
class PantryItem(db.Model):
    __tablename__ = "pantry_items"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    source_item_id = db.Column(db.Integer, db.ForeignKey("source_items.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    expiration_date = db.Column(db.Date, nullable=True)
    source_item = db.relationship("SourceItem")
class GroceryList(db.Model):
    __tablename__ = "grocery_lists"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False, default="My List")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    items = db.relationship("GroceryListItem", backref="list", lazy=True, cascade="all, delete-orphan")
    __table_args__ = (db.Index("ix_active_list_per_user", "user_id", "is_active"),)
class GroceryListItem(db.Model):
    __tablename__ = "grocery_list_items"
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey("grocery_lists.id", ondelete="CASCADE"), nullable=False, index=True)
    source_item_id = db.Column(db.Integer, db.ForeignKey("source_items.id", ondelete="CASCADE"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    checked = db.Column(db.Boolean, nullable=False, default=False)
    source_item = db.relationship("SourceItem")
