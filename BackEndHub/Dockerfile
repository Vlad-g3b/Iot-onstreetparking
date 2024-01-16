# Use the official Python base image
FROM python:3.11

VOLUME /app
# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 5000

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app","--reload","--log-config=log_conf.yaml", "--host", "0.0.0.0", "--port", "5000"]