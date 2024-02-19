# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python manage.py migrate

# Copy the current directory contents into the container at /app
COPY . /app/

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "agify_project.wsgi:application"]
