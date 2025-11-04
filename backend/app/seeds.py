from app import create_app
from app.extensions import db
from app.models import User, Household

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    demo_household = Household(name="McMurray Household")
    db.session.add(demo_household)
    db.session.flush()

    demo_user = User(email="demo@mygrocer.com", household_id=demo_household.id)
    demo_user.set_password("password")
    db.session.add(demo_user)
    db.session.commit()

    print("Seeded demo household and user.")
