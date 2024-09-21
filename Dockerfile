# Use the official Python image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --system --deploy

# Copy the Django project into the container
COPY . .


# Expose the application port
EXPOSE 8000

# Run migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
