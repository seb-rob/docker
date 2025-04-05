# Python MySQL Application with Docker (Same Network)

This project demonstrates how a containerized Python application can communicate with a MySQL database running in a separate Docker container, both within the same custom Docker network (`my-net`). This setup eliminates the need for MySQL to be installed locally on your machine. The MySQL image is pulled from Docker Hub, and both containers are able to communicate with each other using the custom Docker network.

### Python File

Create a Python file called `one_container_to_another.py` and paste the following code. This Python script allows the user to interact with the MySQL database by adding names and displaying all names stored in the database.

```python
import pymysql

def create_connection():
    return pymysql.connect(
        host="mysql-container",  # Hostname for the MySQL container within the same network
        user="root",
        password="root",
        database="userinfo",
    )

# Function to create table to store usernames if it does not exist
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS names (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255)
        )
    """)
    connection.commit()
    cursor.close()

# Function to insert a name into the database
def insert_name(connection, name):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO names (name) VALUES (%s)", (name,))
    connection.commit()

# Function to fetch all names from the database
def fetch_all_names(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM names")
    names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return names

# Main function
def main():
    connection = create_connection()
    create_table(connection)

    while True:
        print("1. Add a name")
        print("2. Show all names")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter a name: ")
            insert_name(connection, name)
            print(f"Name '{name}' added to the database.")
        elif choice == "2":
            names = fetch_all_names(connection)
            if names:
                print("Names in the database: ")
                for name in names:
                    print(name)
            else:
                print("No names found in the database.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    # Close the connection after exiting the loop
    connection.close()

if __name__ == "__main__":
    main()

```

## Set Up MySQL Docker Container

### Pull MySQL Docker Image

To use MySQL in a Docker container, first pull the MySQL image from Docker Hub:

```bash
# Pull mysql image
docker pull mysql

```

### Run MySQL Container with Environment Variables

After the image is pulled, you can run the MySQL container with environment variables to set the root password and the database name:

```bash
# Run MySQL container with environment variables
docker run -d --name mysql-container \
  --network my-net \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=userinfo \
  mysql

```

This will create a MySQL container named `mysql-container` and set the database name to `userinfo`. The MySQL container is also attached to the `my-net` network, allowing it to communicate with other containers on the same network.

### Install Python Package Dependencies

Make sure to install any necessary Python dependencies, including the `cryptography` package, which may be required to avoid runtime errors.

Create a `requirements.txt` file and add the following:

```plaintext
pymysql
cryptography

```

## Dockerfile

Create a Dockerfile in your project’s root directory with the following content:

```Dockerfile
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

```

## Create `.dockerignore` File

The `.dockerignore` file excludes unnecessary files from the Docker image, resulting in a lightweight image. Paste the following into this file:

```plaintext
# Ignore virtual environment folder
venv/
env/
*.venv

# Ignore Python cache files
__pycache__/
*.pyc
*.pyo

# Ignore log files
*.log

# Ignore environment files (e.g., .env) if present
.env

# Ignore IDE-specific files and settings (e.g., VS Code, PyCharm)
.vscode/
.idea/

# Ignore the Dockerfile itself (if not needed in the image)
Dockerfile
.dockerignore

# Ignore the Python package manager lock files (optional)
Pipfile.lock

# Ignore operating system-specific files
.DS_Store
Thumbs.db

# Ignore temporary files created by editors (e.g., vim, emacs)
*.swp
*.bak
*.tmp

# Ignore coverage reports
coverage/

# Ignore tests and test-related files (if not needed in the Docker image)
tests/
test/
*.test.py

# Ignore the README file (if it's not needed in the image)
README.md

```

## Modify Python Code for Containerized MySQL Connection

Since both containers (`python-container` and `mysql-container`) will be running on the same Docker network (`my-net`), modify the connection in your Python code to use the container name (`mysql-container`) as the host.

Update the connection function in `one_container_to_another.py` as follows:

```python
def create_connection():
    return pymysql.connect(
        host="mysql-container",  # Use the container name as the host
        user="root",
        password="root",
        database="userinfo",
    )

```

## Build Docker Image

To build the Docker image, run the following command in your terminal:

```bash
docker build -t mypython-image:1.0 .
```

This command may take a few minutes depending on your internet speed. It will create a new Docker image for your application.

## Run the Application Inside Docker

Once the Docker image is built, run the application inside a Docker container with the following command:

```bash
docker run -it --rm --name python-container --network my-net mypython-image:1.0
```

This command will run your Python application in a container, and it will be able to communicate with the MySQL container because both containers are on the same `my-net` network.


### Additional Network Command

```plaintext
Commands:
  connect     Connect a container to a network
  create      Create a network
  disconnect  Disconnect a container from a network
  inspect     Display detailed information on one or more networks
  ls          List networks
  prune       Remove all unused networks
  rm          Remove one or more networks

Run 'docker network COMMAND --help' for more information on a command.
```