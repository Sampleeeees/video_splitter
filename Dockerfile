# Use the official Python base image
FROM python:3.11-slim

# Set environment variables
ENV POETRY_VERSION=1.9.1
ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN pip install poetry==$POETRY_VERSION

# Set the working directory
WORKDIR /app

# Copy the poetry configuration files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-root --no-dev

# Copy the rest of the application code
COPY . /app/

# Expose the port Streamlit will run on
EXPOSE 8501

# Command to run the application
CMD ["poetry", "run", "streamlit", "run", "app.py"]
