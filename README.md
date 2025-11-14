# MyGrocer

A lightweight grocery and pantry management app designed for real-world use. Track household inventory, add items with quantities and expiration dates, and get recipe suggestions powered by Spoonacular. Built with a Flask/PostgreSQL backend and an Alpine.js + Tailwind frontend deployed on Render and Vercel.

---

## Features

### Core MVP

- User registration and login
- Household-level management (single household for MVP)
- Add pantry items: name, quantity, category, expiration date
- Persistent data using PostgreSQL on Render
- Live deployed backend and frontend
- Recipe suggestions via Spoonacular
- View full recipe details through external links

### Nice-to-Haves Completed

- Color-coded category pills
- Clean Tailwind UI
- Mobile-friendly layout

### Future Features

- Barcode scanning
- Smarter recipe matching using actual pantry items
- Nutrition lookup integration
- Expiration alerts
- AI suggestions for items expiring soon
- Delivery service integrations
- React rebuild once the app scales (componentizing UI, centralized state, smoother navigation)

---

## Tech Stack

**Backend**

- Python
- Flask + Blueprints
- SQLAlchemy
- PostgreSQL (Render)
- JWT authentication
- GitHub Actions CI/CD
- Gunicorn for production

**Frontend**

- HTML
- Alpine.js
- TailwindCSS
- Fetch API
- Vercel deployment

**Third-Party API**

- Spoonacular (recipe suggestions + external recipe views)

---

## Live Links

- **Frontend (Vercel):**  
  <your-frontend-url>

- **Backend (Render):**  
  <your-backend-url>

---

## Local Development

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

flask db upgrade
flask run
```
