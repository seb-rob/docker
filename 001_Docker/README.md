# PROJECT EXECUTION INSTRUCTIONS

## React.js Project Initialization

Assuming you have Node.js installed on your system, follow the steps below to initialize a React.js project. To create the React.js project, execute the following command:

```
npx create-react-app frontend
```

This will create a new directory called frontend with a fresh React project setup.

## Create Dockerfile and .dockerignore File

- Create a Dockerfile in your root directory (inside the frontend project folder) and paste the following code:

```
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy only the package.json and package-lock.json first to leverage Docker cache
COPY package*.json /app/

# Install dependencies using npm ci for a clean and fast installation
RUN npm ci

# Copy the rest of the application code into the container
COPY . .

# Add a non-root user for security purposes
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Change ownership of the application files to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the port your application runs on (e.g., 3000)
EXPOSE 3000

# Start the application
CMD [ "npm", "start" ]
```

- Create a .dockerignore file in your root directory (inside the frontend project folder). This file is used to avoid copying unnecessary files into the Docker image. Paste the following lines into the .dockerignore file:

```
node_modules
.git
.gitignore
Dockerfile
Dockerfile.*
README.md
*.log

```

## Build the Docker Image Using Docker Commands

To build the Docker image for your React project, run the following command from your project directory:

```
docker build -t frontend:01 .
```

This command will create an image named frontend:01. Once the image is ready, verify the build by executing:

```
docker images
```

If you see frontend:01 listed in the output, your image is successfully built

## Run Your Docker Container

Now that the image is built, you can run the container using the following command:

```
docker run -d -p 3000:3000 --name frontendapp frontend:01
```

This command will start the container in detached mode (-d) and map port 3000 of the container to port 3000 on your host machine.

## Verify the Running Project

To check if your React app is running properly in the container, use the following command:

```
docker ps
```

If everything is up and running, you'll see your container listed.

## Troubleshooting

If the project is not running, you can check the container logs for any issues using:

```
docker inspect frontendapp
```

Additionally, to inspect the container in more detail, you can run:

```
docker inspect frontendapp
```

This will provide detailed information about the container and its configuration.

## Additional

```
# To stop the running container
docker stop frontendapp

# To see the list of containers running and stopped
docker ps -a

# To remove stopped containers
docker rm frontendapp

# To list images
docker images

# To delete an image
docker rmi frontend:01
```
