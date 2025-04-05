# Use a smaller base image with Python
FROM python:3-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install the dependencies from the requirements file
RUN pip install -r requirements.txt

# Copy the rest of the application into the container
COPY . .

# Set the command to run the application
CMD ["python", "sql.py"]
