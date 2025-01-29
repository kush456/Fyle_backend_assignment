# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=core/server.py
ENV FLASK_ENV=development

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]