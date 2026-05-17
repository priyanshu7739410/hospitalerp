# Docker Commands

### 1. Start and Build Containers in Background
**Command:** `docker compose up --build -d`
**When to use:** Whenever you change the `Dockerfile`, `docker-compose.yml`, or `requirements.txt`, or when you are starting the environment for the first time.
**What it does:** Builds the Docker images from scratch and starts the containers in detached (background) mode.

### 2. View Container Logs
**Command:** `docker compose logs -f api`
**When to use:** When you want to see the output, errors, or requests happening inside your FastAPI application.
**What it does:** The `-f` stands for "follow". It streams the live logs of the `api` container to your terminal. Press `Ctrl+C` to stop watching the logs (this won't stop the container, just the log stream).

---

# Database Commands (Alembic)

### 3. Initialize Alembic (Run inside Docker)
**Command:** `docker compose exec api alembic init alembic`
**When to use:** Only ONCE at the very beginning of the project to set up the migration folders.
**What it does:** `exec api` tells Docker to run a command inside the running `api` container. `alembic init alembic` creates an `alembic/` folder and an `alembic.ini` file which will manage our database versions.

### 4. Generate a New Migration Script
**Command:** `docker compose exec api alembic revision --autogenerate -m "create_patients_table"`
**When to use:** Whenever you create a new model or change an existing model (like adding a column).
**What it does:** Alembic inspects your Python models, compares them to the active PostgreSQL database, and writes an automatic Python script inside `alembic/versions/` detailing exactly how to update the database.

### 5. Apply Migrations to Database
**Command:** `docker compose exec api alembic upgrade head`
**When to use:** Immediately after generating a migration script, or when pulling new code from GitHub.
**What it does:** Executes the migration scripts against PostgreSQL, physically creating or updating the tables.
