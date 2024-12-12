import sqlite3

DB_PATH = "Database/rps_game.db"

def add_users():
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert 10 users into the User table
    for i in range(1, 11):
        username = f"user{i}"
        password = f"password{i}"
        try:
            cursor.execute("INSERT INTO User (username, password) VALUES (?, ?)", (username, password))
            print(f"Added: {username} with password {password}")
        except sqlite3.IntegrityError:
            print(f"User {username} already exists. Skipping.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("10 users added successfully!")


def populate_games():
    """
    Populate the Game table with 2 games for each user.
    One game will be won by the user, the other by the computer.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Fetch all user IDs and usernames
        cursor.execute("SELECT userid, username FROM User;")
        users = cursor.fetchall()

        if not users:
            print("No users found in the database. Please add users first.")
            return

        # Insert 2 games for each user
        for user in users:
            userid, username = user

            # Game 1: User wins
            cursor.execute("""
                INSERT INTO Game (firstto, winner, userid)
                VALUES (?, ?, ?);
            """, (3, username, userid))

            # Game 2: Computer wins
            cursor.execute("""
                INSERT INTO Game (firstto, winner, userid)
                VALUES (?, ?, ?);
            """, (3, "Computer", userid))

            print(f"Inserted 2 games for user: {username} (ID: {userid})")

        # Commit changes and close the connection
        conn.commit()
        print("Games have been successfully populated!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    add_users()
    populate_games()
