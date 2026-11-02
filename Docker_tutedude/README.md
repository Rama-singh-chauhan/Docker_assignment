# Dockerized Full-Stack App — Express Frontend + Flask Backend

A course-registration form built with **Node.js/Express** (frontend) that sends its data to a **Flask** API (backend). Both services are containerized with Docker and connected on a shared network using Docker Compose.

**Author:** Ajay Kumar

## Architecture

```
 Browser ──► Express frontend (port 3000) ──POST /submit (JSON)──► Flask backend (port 5000)
                      ▲                                                     │
                      └──────────────── JSON response ◄─────────────────────┘
            (both containers on the "app-network" bridge network; the frontend
             reaches the backend by its service name: http://backend:5000)
```

## Project structure

```
Docker_AjayKumar/
├── backend/
│   ├── app.py              # Flask API: /, /health, /submit, /submissions
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── server.js           # Express server: serves form, forwards to Flask
│   ├── package.json
│   ├── package-lock.json
│   ├── views/              # EJS templates (form + success page)
│   ├── public/style.css
│   ├── Dockerfile
│   └── .dockerignore
├── docker-compose.yaml     # runs both services on app-network
├── .env.example            # DOCKERHUB_USERNAME=...
├── .gitignore              # node_modules, venv, .vscode, .env, ...
└── README.md
```

## Run with Docker Compose

```bash
# 1. Set your Docker Hub username (used to tag the images)
cp .env.example .env        # then edit DOCKERHUB_USERNAME in .env

# 2. Build and start both containers
docker compose up --build -d

# 3. Check they're running
docker compose ps
```

Open **http://localhost:3000**, fill in the form and submit. The backend can be checked directly at http://localhost:5000/health and http://localhost:5000/submissions.

Stop everything with `docker compose down`.

## Push images to Docker Hub

```bash
docker login
docker compose build
docker compose push
```

This pushes `<username>/flask-backend:latest` and `<username>/express-frontend:latest`.

## Push code to GitHub

```bash
git init
git add .
git commit -m "Dockerized Express frontend and Flask backend"
git branch -M main
git remote add origin https://github.com/<username>/Docker_AjayKumar.git
git push -u origin main
```

## Run without Docker (development)

```bash
# backend
cd backend && pip install -r requirements.txt && python app.py
# frontend (in a second terminal)
cd frontend && npm install && BACKEND_URL=http://localhost:5000 npm start
```

## API

| Method | Route          | Description                                  |
|--------|----------------|----------------------------------------------|
| GET    | `/health`      | Health check used by Docker Compose          |
| POST   | `/submit`      | Validates and stores a form submission (JSON or form data) |
| GET    | `/submissions` | Lists all submissions received so far        |

## Links

- GitHub: `https://github.com/<username>/Docker_AjayKumar`
- Docker Hub: `https://hub.docker.com/r/<username>/flask-backend`, `https://hub.docker.com/r/<username>/express-frontend`
