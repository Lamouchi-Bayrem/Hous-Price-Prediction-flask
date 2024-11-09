# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Alternatively, you can manually install the packages like this:
RUN pip install Flask scikit-learn numpy pandas gunicorn

# Expose the port the app runs on
EXPOSE 5001

# Define environment variable to avoid Python buffering
ENV PYTHONUNBUFFERED 1

# Run the Flask app
CMD ["python", "app.py"]
CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]