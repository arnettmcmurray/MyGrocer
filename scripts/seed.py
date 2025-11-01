from backend.app import create_app
from backend.extensions import db
from backend.models import User, List, Item, Recipe
from backend.utils import hash_password

app = create_app()
with app.app_context():
    db.create_all()  # ensure tables exist

    # demo user + default lists
    if not User.query.filter_by(email="demo@example.com").first():
        u = User(email="demo@example.com", password_hash=hash_password("password"), name="Demo")
        db.session.add(u); db.session.flush()
        for ln in ["Pantry","Fridge","Freezer","Grocery"]:
            db.session.add(List(name=ln, user_id=u.id))
        db.session.flush()
        p = List.query.filter_by(user_id=u.id, name="Pantry").first()
        fr = List.query.filter_by(user_id=u.id, name="Fridge").first()
        fz = List.query.filter_by(user_id=u.id, name="Freezer").first()
        items = [
            (Item(name="milk", quantity=1, storage_area="fridge"), fr),
            (Item(name="eggs", quantity=6, storage_area="fridge"), fr),
            (Item(name="pasta", quantity=2, storage_area="pantry"), p),
            (Item(name="tomato sauce", quantity=1, storage_area="pantry"), p),
            (Item(name="rice", quantity=1, storage_area="pantry"), p),
            (Item(name="chicken", quantity=2, storage_area="freezer"), fz),
        ]
        for it, lst in items:
            db.session.add(it); db.session.flush(); lst.items.append(it)
        db.session.flush()

    # recipes
    if not Recipe.query.first():
        seeds = [
            {"title":"Veggie Omelet","total_minutes":15,"difficulty":"easy",
             "ingredients_json":[{"name":"eggs","qty":3},{"name":"milk","qty":1},{"name":"spinach","qty":1,"optional":True}],
             "steps_json":{"steps":["Beat eggs","Add milk","Cook with spinach"]}},
            {"title":"Pasta Marinara","total_minutes":25,"difficulty":"easy",
             "ingredients_json":[{"name":"pasta","qty":1},{"name":"tomato sauce","qty":1},{"name":"garlic","qty":1,"optional":True}],
             "steps_json":{"steps":["Boil pasta","Heat sauce","Combine"]}},
            {"title":"Chicken Stir Fry","total_minutes":30,"difficulty":"medium",
             "ingredients_json":[{"name":"chicken","qty":2},{"name":"rice","qty":1},{"name":"mixed veggies","qty":2}],
             "steps_json":{"steps":["Cook rice","Stir-fry chicken","Add veggies"]}},
        ]
        for r in seeds:
            db.session.add(Recipe(title=r["title"], total_minutes=r["total_minutes"], difficulty=r["difficulty"],
                                  ingredients_json=r["ingredients_json"], steps_json=r["steps_json"]))
    db.session.commit()
    print("Seed complete")
