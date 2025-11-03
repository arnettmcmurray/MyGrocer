from . import create_app
from .db_utils import init_db, seed_db
if __name__ == "__main__":
    app = create_app()
    init_db(app)
    seed_db(app)
    print("Seed complete.")
