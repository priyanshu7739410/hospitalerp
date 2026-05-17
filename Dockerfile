# Step 1: Base Image
# We use the official Python 3.11 image. "slim" means it doesn't have extra OS tools we don't need, making the image smaller and faster to pull.
FROM python:3.11-slim

# Step 2: Environment Variables
# Prevent Python from writing .pyc files (byte-compiled code) to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure Python outputs everything directly to the terminal without buffering (useful for real-time logging)
ENV PYTHONUNBUFFERED 1

# Step 3: Working Directory
# This is like running 'mkdir /app' and 'cd /app' inside the container.
WORKDIR /app

# Step 4: Install System Dependencies
# PostgreSQL requires some underlying C libraries to build the psycopg2 adapter.
# We update apt, install them, and then clean up to keep the image small.
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Install Python Dependencies
# We copy the requirements file first, BEFORE copying the rest of our code.
# Why? Docker caches layers. If we only change our python code, Docker won't reinstall all dependencies.
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Step 6: Copy Application Code
# Now we copy all our actual code into the /app directory inside the container.
COPY . /app/

# Step 7: Run the Application
# We use Uvicorn (an ASGI server) to run our FastAPI application.
# It will look for the 'app' folder, inside it the 'main.py' file, and the 'app' instance inside that file.
# We bind it to 0.0.0.0 so it is accessible from outside the container, on port 8000.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
