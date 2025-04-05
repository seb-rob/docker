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