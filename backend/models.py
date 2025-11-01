from datetime import datetime, date
from typing import List as TList, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Date, JSON, Table
from backend.extensions import db

# List <-> Item association
list_items = Table(
    "list_items",
    db.metadata,
    db.Column("list_id", db.Integer, db.ForeignKey("lists.id"), primary_key=True),
    db.Column("item_id", db.Integer, db.ForeignKey("items.id"), primary_key=True),
    db.Column("added_at", db.DateTime, default=datetime.utcnow, nullable=False),
)

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    lists: Mapped[TList["List"]] = relationship("List", back_populates="user", cascade="all, delete-orphan")
    plans: Mapped[TList["PlanEntry"]] = relationship("PlanEntry", back_populates="user", cascade="all, delete-orphan")

class List(db.Model):
    __tablename__ = "lists"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    notes: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="lists")
    items: Mapped[TList["Item"]] = relationship("Item", secondary=list_items, back_populates="lists")

class Item(db.Model):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    reserved_qty: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(120))
    storage_area: Mapped[Optional[str]] = mapped_column(String(20))  # pantry|fridge|freezer
    upc: Mapped[Optional[str]] = mapped_column(String(32), index=True)
    expiration_date: Mapped[Optional[date]] = mapped_column(Date)
    nutrition_json: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    lists: Mapped[TList["List"]] = relationship("List", secondary=list_items, back_populates="items")

class Recipe(db.Model):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    total_minutes: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), default="easy")  # easy|medium|hard
    ingredients_json: Mapped[dict] = mapped_column(JSON, default=dict)  # [{"name","qty","optional":bool}]
    steps_json: Mapped[dict] = mapped_column(JSON, default=dict)        # {"steps":[...]}
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

class PlanEntry(db.Model):
    __tablename__ = "plan_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), index=True)
    day: Mapped[date] = mapped_column(Date, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="plans")
    recipe: Mapped["Recipe"] = relationship("Recipe")
