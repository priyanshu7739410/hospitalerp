import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Step 1: Construct the Database URL
# We read the credentials injected by docker-compose from our .env file.
# The format is: postgresql://user:password@host:port/database_name
POSTGRES_USER = os.getenv("POSTGRES_USER", "hospital_admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "hospital_secure_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "hospital_erp")
# Notice the host is "db", which is the exact name of the PostgreSQL service in docker-compose.yml!
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Step 2: Create the SQLAlchemy Engine
# The engine is the "bridge" or connection manager between our Python app and the PostgreSQL database.
# We don't interact with the engine directly to run queries; it just handles the networking and connection pooling under the hood.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Step 3: Create the SessionLocal Factory
# sessionmaker creates a blueprint (factory) for creating database sessions.
# A "session" is like a temporary, isolated conversation with the database.
# autocommit=False: We want to manually say when to save data, to avoid saving half-complete transactions.
# autoflush=False: We don't want SQLAlchemy to preemptively push queries to the DB before we explicitly tell it to.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Step 4: Dependency Injection Function
# FastAPI will use this function to give every incoming API request its own fresh session.
# Using 'yield' ensures that once the request is done, the 'finally' block runs and closes the connection, returning it to the pool.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
