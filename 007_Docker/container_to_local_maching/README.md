# Python MySQL Application with Docker

This project demonstrates how a containerized Python application can communicate with a MySQL database running on the local machine (not in the container). It also explains how data is stored persistently even if the container is destroyed. This guide assumes that you already have MySQL installed and running on your local machine.

## Python File

Create a Python file called `sql.py` and paste the following code. This Python script presents the user with a choice of actions, and based on the selection, it interacts with the MySQL database.

```python
import pymysql

def create_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="YOUR_DB_PASSWORD",
        database="userinfo",
    )

# Function to create table to store usernaems if it does not exists
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

# main function
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

## Run the Application

To run this program locally (without Docker), execute the following command in your terminal (ensure that the required libraries are installed):

```bash
python sql.py
```

Before running the program, make sure you have the requirements.txt file with the following content:

```plaintext
pymysql
```

And install the dependencies using `pip install -r requirements.txt`


## Dockerfile

Create a `Dockerfile` in your root directory and paste the following code:

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

## Build Docker Image

To build the Docker image, execute the following command in your terminal:

```bash
docker build -t mypyapp:1.0 .
```

This command may take a few minutes depending on your internet connection. It will create a new Docker image for your application.

## Create Container

Next, run the application inside a Docker container by executing the following command:

```bash
docker run -it --rm --name pysqlapp mypyapp:1.0
```

### Handling the Connection Error

When you run the container, you may encounter the following error:

```arduino
File "/usr/local/lib/python3.13/site-packages/pymysql/connections.py", line 649, in connect
    sock = socket.create_connection(
        (self.host, self.port), self.connect_timeout, **kwargs
    )
  File "/usr/local/lib/python3.13/socket.py", line 864, in create_connection
    raise exceptions[0]
  File "/usr/local/lib/python3.13/socket.py", line 849, in create_connection
    sock.connect(sa)
    ~~~~~~~~~~~~^^^^
ConnectionRefusedError: [Errno 111] Connection refused

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/app/sql.py", line 70, in <module>
    main()
    ~~~~^^
  File "/app/sql.py", line 39, in main
    connection = create_connection()
  File "/app/sql.py", line 4, in create_connection
    return pymysql.connect(
           ~~~~~~~~~~~~~~~^
        host="localhost",
        ^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        database="userinfo",
        ^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/usr/local/lib/python3.13/site-packages/pymysql/connections.py", line 361, in __init__
    self.connect()
    ~~~~~~~~~~~~^^
  File "/usr/local/lib/python3.13/site-packages/pymysql/connections.py", line 716, in connect
    raise exc
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on 'localhost' ([Errno 111] Connection refused)")

```
The error says that **"Can't connect to MySQL server on 'localhost'**. This error occurs because the container is an isolated environment and cannot access the MySQL server running on your local machine by default. To fix this, you need to update the host in the create_connection function in sql.py.

### Solution

Change the `host="localhost"` to `host="host.docker.internal"`. This will ensure the container can access the MySQL server running on your host machine.


```python
def create_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="YOUR_DB_PASSWORD",
        database="userinfo",
    )
```

## Final sql.py File

After the changes, your sql.py file should look like this:

```python
import pymysql

def create_connection():
    return pymysql.connect(
        host="host.docker.internal",
        user="root",
        password="YOUR_DB_PASSWORD",
        database="userinfo",
    )

# Function to create table to store usernaems if it does not exists
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

# main function
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

## Final Run and Test


After making the changes to `sql.py`, rebuild the Docker image and run the application again.

```bash
# Build Docker image
docker build -t mypyapp:2.0 .

# Run the application
docker run -it --rm --name pymysqlapp mypyapp:2.0

```

This should now work seamlessly, allowing you to interact with the MySQL database running on your local machine.

