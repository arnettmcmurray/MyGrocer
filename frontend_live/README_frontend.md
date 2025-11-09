# MyGrocer Frontend (Alpine + Tailwind)

## Local Development

1. Open a terminal at the project root.
2. Start your backend (Flask) on port 5000:
   flask run --port 5000
3. In another terminal, serve the frontend:
   cd frontend_live
   python3 -m http.server 5173
4. Open http://127.0.0.1:5173 in your browser.

## API Connection

The frontend calls your Flask backend at:
http://127.0.0.1:5000/api/v1

You can change this in /js/ui.js under the `API_BASE` variable.

## Pages

| Page            | Description                                  |
| --------------- | -------------------------------------------- |
| index.html      | Home page / API health check / token preview |
| login.html      | Register & login, saves JWT to localStorage  |
| pantry.html     | CRUD pantry items (GET/POST/DELETE)          |
| households.html | CRUD households                              |
| recipes.html    | Placeholder for /foodref feature             |

## Deployment to Vercel

1. Log into [vercel.com](https://vercel.com).
2. Create a new project and import this folder (`frontend_live`).
3. Framework preset: "Other" → Output directory: `frontend_live`.
4. Once deployed, set the correct API base for your hosted backend in the browser console:
