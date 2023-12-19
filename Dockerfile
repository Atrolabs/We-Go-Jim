# Use an official Python runtime as a parent image
FROM python:latest

# Copy the entire project into the container at /we-go-jim
COPY . /we-go-jim/

# Switch to the /we-go-jim directory
WORKDIR /we-go-jim

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["python", "run.py"]
