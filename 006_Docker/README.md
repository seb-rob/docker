# ReactJS Project with Docker Bind Mounts

This project demonstrates how to use Docker bind mounts with a ReactJS application. By using bind mounts, we can link the local file system with the container, allowing us to persist changes to the application code while the container is running.

## Project Setup

### 1. Create the ReactJS Project

If you don't already have a ReactJS project, you can easily create one using `create-react-app`. Here's how:

```bash
npx create-react-app react-docker-app
cd react-docker-app
```
### 2. Create Dockerfile

The `Dockerfile` defines the steps to build the Docker image for your ReactJS app. Here is the Dockerfile for the ReactJS application:

```Dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . ./

CMD [ "npm", "start" ]

```

### 3. Create .dockerignore

To ensure we don't copy unnecessary files into the Docker image, create a .dockerignore file and paste the following content:

```plaintext
# See https://help.github.com/articles/ignoring-files/ for more about ignoring files.

# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# production
/build

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*

```

### 4. Running React App with Bind Mounts

To run the React app in Docker and bind mount your local project directory to the container, use the following command:

```bash
docker run -d -p 3000:3000 --name reactapp --rm -v $(pwd):/app react-docker-app:1.0
```

### Important Notes:

- `$(pwd)` will get the current directory's path in Linux and macOS. On Windows, you may need to adjust the path format (e.g., `C:/path/to/your/project`).
- The `-v $(pwd):/app` flag mounts the current working directory (`$(pwd)`) on your machine to the `/app` directory in the container.
- The container will run in the background (`-d`), exposing port 3000 to access the React app at `http://localhost:3000`.


### 5. Viewing the Application

Once the container is running, open your web browser and navigate to `http://localhost:3000`. You should see your ReactJS app running.

### 6. Development Workflow with Bind Mounts

With bind mounts in place, you can modify the source code of your React app on your local machine, and the changes will immediately be reflected in the running container without needing to rebuild the Docker image or restart the container.

This enables a seamless development experience as you can edit your code locally and instantly see the changes in the running Docker container.

