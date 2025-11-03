from .extensions import db
from .models import User, Category, SourceItem, PantryItem, GroceryList, GroceryListItem
def init_db(app):
    with app.app_context():
        db.create_all()
def seed_db(app):
    with app.app_context():
        if User.query.first():
            return
        u1 = User(email="demo1@example.com"); u1.set_password("password")
        u2 = User(email="demo2@example.com"); u2.set_password("password")
        db.session.add_all([u1, u2]); db.session.commit()
        cats = [Category(user_id=u1.id, name=n) for n in ["Produce", "Dairy", "Snacks"]]
        db.session.add_all(cats); db.session.commit()
        items = [
            SourceItem(user_id=u1.id, name="Bananas", category_id=cats[0].id),
            SourceItem(user_id=u1.id, name="Milk", category_id=cats[1].id),
            SourceItem(user_id=u1.id, name="Yogurt", category_id=cats[1].id),
            SourceItem(user_id=u1.id, name="Chips", category_id=cats[2].id),
            SourceItem(user_id=u1.id, name="Apples", category_id=cats[0].id),
            SourceItem(user_id=u1.id, name="Bread", category_id=None),
        ]
        db.session.add_all(items); db.session.commit()
        from datetime import date, timedelta
        p1 = PantryItem(user_id=u1.id, source_item_id=items[0].id, quantity=3, expiration_date=date.today() + timedelta(days=5))
        p2 = PantryItem(user_id=u1.id, source_item_id=items[1].id, quantity=1, expiration_date=None)
        db.session.add_all([p1, p2]); db.session.commit()
        gl = GroceryList(user_id=u1.id, name="My List", is_active=True)
        db.session.add(gl); db.session.commit()
        gli = GroceryListItem(list_id=gl.id, source_item_id=items[4].id, quantity=4, checked=False)
        db.session.add(gli); db.session.commit()
