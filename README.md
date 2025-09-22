# note-keeper-22956-22965

Backend (Flask) for Note Keeper app.

How to run locally:
1. cd note_backend
2. Create a virtual environment and install requirements:
   - python -m venv .venv && source .venv/bin/activate
   - pip install -r requirements.txt
3. Copy .env.example to .env and set SECRET_KEY
4. Run the server:
   - python run.py
5. API docs available at /docs (e.g., http://localhost:3001/docs)

Key endpoints:
- GET /           -> health
- POST /auth/signup {email,password} -> {token}
- POST /auth/login {email,password}  -> {token}
- GET /notes/     -> list notes (Authorization: Bearer <token>)
- POST /notes/    -> create note (Authorization header required)
- GET /notes/{id}
- PATCH /notes/{id}
- DELETE /notes/{id}