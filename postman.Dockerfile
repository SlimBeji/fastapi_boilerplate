# Base Image
FROM python:3.9

# Create Working directory
WORKDIR /app

# Copying requirements
COPY ./requirements.txt /app/requirements.txt
COPY ./requirements-dev.txt /app/requirements-dev.txt

# Updating pip and installing dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

# Copy Code
COPY ./backend /app/backend
COPY ./frontend /app/frontend
COPY main.py /app/main.py

# Entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
