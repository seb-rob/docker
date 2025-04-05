
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