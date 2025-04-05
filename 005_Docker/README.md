# Project Execution

This project demonstrates how Docker volumes are used. In this project, you'll notice that the Python program writes the username to the user_info.txt file. It works perfectly without containerizing the app (meaning it stores previously given usernames). However, when we containerize the app, every time the container is started, it only stores the current username, and the previously entered usernames are lost. This is where volumes come into play, as they allow you to persist data (like usernames) even after the container stops.

## Simple Python Project

First, create a Python file `mypyapp.py` with the following code. This program takes input from the user and writes the username to `user_info.txt`:

```python

# take input (username) from user
username = input("Enter your username: ")

# write username in file
if username:
    with open("user_info.txt", "a") as file:
        file.write(username + "\n")

# print all usernames if users input is 'y'
usernames = input("Do you want to view all usernames (y/n): ")
if usernames == 'y':
    try:
        with open("user_info.txt", "r") as file:
            content = file.readlines()
    except Exception as e:
        print(e, type(e))
    else:
        for line in content:
            print(f"{line.rstrip()}")
```

## Create an Empty `user_info.txt` File

To create an empty file `user_info.txt`, run the following command:

```bash
touch user_info.txt
```

## Create `.dockerignore` Files

Next, create a `.dockerignore` file to avoid adding unnecessary files to your Docker image. Run the following command:

```bash
touch .dockerignore
```

Then paste the following content into `.dockerignore`:

```plaintext
# Ignore virtual environment folder
venv/

# Ignore Python cache files
__pycache__/
*.pyc
*.pyo

# Ignore log files
*.log

# Ignore environment files (e.g., .env) if present
.env

# Ignore any IDE-specific files or settings
.vscode/
.idea/

# Ignore user-specific files (e.g., user_info.txt)
user_info.txt

# Ignore any backup or temporary files created by editors (e.g., vim, emacs)
*.swp
*.bak
*.tmp

# Ignore the Dockerfile itself (if not needed in the image)
Dockerfile
.dockerignore

# Ignore package manager lock files (optional)
Pipfile.lock
requirements.txt

# Ignore operating system-specific files
.DS_Store
Thumbs.db

```

## Create `Dockerfile` to Build the Docker Image

Create the `Dockerfile` with the following content. It specifies how to build your Docker image.

```Dockerfile
FROM python:3-alpine3.10

WORKDIR /app

COPY . .

CMD [ "python", "mypyapp.py" ]

```

## Test Your Program Before Creating Docker Image and Containers

Before creating the Docker image and container, test your Python program by running it with the following command:

```bash
python mypyapp.py
```
Enter a username, and when prompted, type y to view all usernames. You should see all previously entered usernames (if ran prgram more than once).

## Build the Docker Image

To build the Docker image, run the following command:

```bash
docker build -t pyapp:1.0 .
```

After building, you can verify the image was created by running `docker images`.

## Create Docker Container and Run Your Program in `-it` Mode

Since your program takes user input, you need to run the container in interactive mode (`-it`). Run the following command to start the container:

```bash
docker run -it --name pythonapp pyapp:1.0
```

If you execute this program multiple times, you'll notice that it only shows the current username and doesn't retain previous usernames.

## Use Volumes to Persist Data

To persist the usernames (and not lose previously entered data), you can use Docker volumes. Run the following command to create a volume and mount it to your container:

```bash
docker run -it --name pythonapp -v myvolume:/app/ pyapp:1.0
```

Now, when you run the program again, it will retain the previously entered usernames. 

## Additional Commands for Managing Docker Volumes

Here are some additional commands you can use to manage Docker volumes:

```plaintext
Commands:
  create      Create a volume
  inspect     Display detailed information on one or more volumes
  ls          List volumes
  prune       Remove unused local volumes
  rm          Remove one or more volumes

Run 'docker volume COMMAND --help' for more information on a command.
```