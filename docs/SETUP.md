# Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -c "from backend.app import create_app; from backend.extensions import db; app=create_app();\
\nfrom contextlib import suppress;\
\nwith app.app_context(): db.create_all(); print('DB ready')"
python backend/app.py
