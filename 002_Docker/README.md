# PROJECT EXECUTION INSTRUCTIONS
This Python program adds two user-input numbers and outputs the result. Since this program requires user interaction (input), the Docker container must be executed in interactive mode.

## Create Isolated Virtual Environment for Python Program
Assuming you have Python installed on your system, follow these steps to create an isolated virtual environment:
- Create the virtual environment by running the following command:
```
python -m venv virual-enviroment
```
- Activate the virtual environment:
```
source virual-enviroment/Scripts/activate
```
Now your virtual environment is activated, and you can install any dependencies inside this isolated environment. However, note that when using Docker, creating a virtual environment inside the container is typically unnecessary because Docker itself isolates the application.

## Create .dockerignore and .gitignore
- Create a .dockerignore file in your root directory. This file is used to avoid copying unnecessary files into the Docker image. Paste the following content into the .dockerignore file:
```
.git
.gitignore
Dockerfile
Dockerfile.*
README.md
*.log
```
- Create a .gitignore file to ensure unnecessary files are not pushed to your Git repository. Paste the following content into the .gitignore file:
```
# Ignore Python cache files
__pycache__/
*.pyc
*.pyo

# Ignore virtual environments
venv/
.env/

# Ignore IDE/editor files
.vscode/
.idea/

# Ignore Docker-related files
Dockerfile
Dockerfile.*

# Ignore logs
*.log

# Ignore system-specific files
.DS_Store
Thumbs.db

```
## Create Docekrfile
Create a Dockerfile in your root directory and paste the following content:
```
# Use an official Python runtime as a parent image
FROM python:3-alpine3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Create a non-root user for better security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Change the ownership of the files to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Run the Python program when the container starts
CMD [ "python", "addition.py" ]
```

## Build Docker Image for Your Python Program
To build the Docker image for your Python program, execute the following command:
```
docker build -t sumapp:01 .
```
Once the build process completes, verify that the image was created by running:
```
docker images
```
This will list all Docker images, and you should see sumapp:01 listed.

## Run Docker Container
To run the Docker container interactively (since the program requires user input), use the following command:
```
docker run -it --name sumapp-container sumapp:01
```
The ```-it``` flag ensures that the container runs interactively and allows you to provide input directly. Since the program asks for two numbers to perform the addition, interactive mode is necessary for it to function properly.
