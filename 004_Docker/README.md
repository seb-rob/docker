# Project Execution and Publishing Docker Image to Docker Hub

This project demonstrates how to create a Docker image, execute it, and push the Docker image to a Docker Hub repository.

## 1. Create ```server.js``` File

Below is the code that runs a simple Express server:

```Server.js
const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
```

## 2. Add ```.dockerignore``` and ```.gitignore``` Files

- **.dockerignore:** Create `.dockerignore` file and paste the following code:


```plaintext
# Ignore node_modules because it will be rebuilt inside the container
node_modules

# Ignore log files
*.log

# Ignore Dockerfile and other Docker-related files
Dockerfile
.dockerignore

# Ignore the .git directory
.git

# Ignore the build output (if applicable)
dist
build

# Ignore any temporary files or IDE settings (e.g., VS Code)
.vscode
.idea
*.swp

# Ignore package-lock.json to avoid potential conflicts (you might want to keep this)
package-lock.json

# Ignore any environment variable files if you don't want them in the Docker image
.env

```

- **.gitignore**: Create .gitignore file and paste the following code:


```plaintext
# Ignore node_modules directory
node_modules/

# Ignore log files
*.log

# Ignore environment variable files (if applicable)
.env

# Ignore the package-lock.json (optional, you can decide to keep it)
package-lock.json

# Ignore any temporary files or IDE settings (e.g., VS Code)
.vscode/
.idea/

# Ignore build or dist directories if you are building files
dist/
build/

# Ignore npm-debug logs
npm-debug.log*

# Ignore operating system files
.DS_Store
Thumbs.db

# Ignore test coverage reports (if any)
coverage/

# Ignore any other unnecessary files
*.swp
*.bak

```
## 3. Create `Dockerfile`

Create a `Dockerfile` and paste the following code:

```Dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY . .

RUN addgroup -S appgroup && adduser -S appuser -G appgroup && chown -R appuser:appgroup /app

USER appuser

EXPOSE 3000

CMD [ "npm", "start" ]
```

## 4. Create Docker Image

To create the Docker image, execute the following command:

```bash
docker build -t username/dockerimage:tag .
```

This command will create a Docker image with the name `username/dockerimage` and the specified `tag`.


## 5. Create a Container and Verify Everything is Working

Create a container by running the Docker image:

```bash
docker run -d -p 3000:3000 --rm --name anyname username/dockerimage:tag
```

This will create a container. You can check if everything is running as expected by visiting `http://localhost:3000` in your browser. You should see the "Hello World!" message.


## 6. Push the Image to Docker Hub Repository

To push the image to your Docker Hub repository, execute the following commands:

```bash

# login using browser
docker login

# alternative for login using username and password
docker login -u username

# push the code to your repo
docker push username/dockerimage:tag

```

## 7. To Check if Your Image is Working Fine

To check if your image is working properly after pushing it to Docker Hub, follow these steps:

- Pull the image from Docker Hub to your local development environment and run the docker container

```bash
# pull the iamge
docker pull username/dockerimage:tag

# run the docker container
docker run -d -p 3000:3000 --rm --name anyname username/dockerimage:tag
```

