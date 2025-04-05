# Portfolio Project Documentation

This README outlines the steps to set up and deploy a basic portfolio website in a Docker container. The portfolio includes a simple index.html file and is served using an Nginx web server running inside a Docker container.

## Project Overview

This project consists of the following:
- **index.html**: The HTML file that represents the portfolio.
- **Dockerfile**: Configuration file to build a Docker image that serves the portfolio using Nginx.
- **.dockerignore**: Specifies files to exclude from the Docker image.
- **.gitignore**: Specifies files and directories to exclude from Git version control.

### File Structure

```plaintext
.
├── Dockerfile
├── .dockerignore
├── .gitignore
├── index.html
└── README.md
```

### Dockerfile

The Dockerfile defines the steps for building a Docker image that serves the portfolio using Nginx. It starts from the official Nginx image and copies the ```index.html`` file into the appropriate directory.

```Dockerfile
# Use the official Nginx image as the base
FROM nginx:alpine

# Copy the index.html into the default Nginx directory
COPY index.html /usr/share/nginx/html/index.html

# Expose port 80 to access the web page
EXPOSE 80
```

### .dockerignore

This file tells Docker which files to ignore when building the image. It helps to keep the Docker image lean by excluding unnecessary files and directories such as ```.git``` or log files.

```plaintext
.git
.gitignore
Dockerfile
Dockerfile.*
README.md
*.log
```

### .gitignore

This file ensures that unwanted files and directories are excluded from version control when you commit to Git.

```plaintext
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

## Building and Running the Docker Container

### Step 1: Build the Docker Image

To build the Docker image, navigate to the directory where your ```Dockerfile``` and other project files are located and run the following command:

```bash
docker build -t portfolio-app:1.0 .
```

This will create a Docker image with the tag ```portfolio-app:1.0```.

### Step 2: Run the Docker Container

To run the Docker container, execute the following command:

```bash
docker run -d --rm -p 8080:80 --name portfolio-container portfolio-app:1.0
```

- ```-d``` runs the container in detached mode.
- ```-p 8080:80``` maps port 80 of the container to port 8080 on your host.
- ```--name``` portfolio-container assigns the container a name.
- ```portfolio-app:1.0``` is the name of the image you built.
- ```--rm``` flag in Docker is used to automatically remove the container when it stops. This helps avoid accumulating stopped containers that are no longer needed.

You can now access your portfolio by navigating to ```http://localhost:8080``` in your web browser.

