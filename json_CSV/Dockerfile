# Use an official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy your app files into the container
COPY app.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 5000
# Run the app
CMD ["python", "app.py"]
``