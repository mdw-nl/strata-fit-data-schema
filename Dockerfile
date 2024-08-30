# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements file to install dependencies first
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to /app
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable to store the mode in which the app runs
ENV MODE=production

# Run main.py from the api directory when the container launches using gunicorn as the WSGI server
CMD ["gunicorn", "api.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
