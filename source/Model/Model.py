import sqlite3
import os
from Model.queries import *

class Model:
    def __init__(self, db_path=None):
        """
        Initialize the Model class with the database path.
        """
        # Default database location inside 'database' folder
        self.db_path = db_path or os.path.join("database", "rps_game.db")

        # Ensure the database file and folder exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._initialize_tables()

    def _connect(self):
        """
        Private method to connect to the SQLite database.
        """
        return sqlite3.connect(self.db_path)

    def _initialize_tables(self):
        """
        Initializes the User and Game tables if they don't exist.
        """
        create_user_table = """
        CREATE TABLE IF NOT EXISTS User (
            userid INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        """
        create_game_table = """
        CREATE TABLE IF NOT EXISTS Game (
            gameid INTEGER PRIMARY KEY AUTOINCREMENT,
            firstto INTEGER NOT NULL,
            winner TEXT,
            userid INTEGER NOT NULL,
            FOREIGN KEY (userid) REFERENCES User(userid)
        );
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(create_user_table)
            cursor.execute(create_game_table)
            conn.commit()

    # Create a new user
    def create_user(self, username, password):
        with self._connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(INSERT_NEW_USER, (username, password))
                conn.commit()
                print(f"User '{username}' created successfully!")
            except sqlite3.IntegrityError:
                print(f"Error: User '{username}' already exists.")

    # Get user's id
    def get_userid(self, username):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(GET_USER_ID, (username,))
            result = cursor.fetchone()
            return result[0] if result else None
        
    # Check if a user exists
    def check_user_existence(self, username):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(CHECK_USER_EXISTENCE, (username,))
            return cursor.fetchone() is not None

    # Get a user's password by username
    def get_user_password(self, userid):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(GET_USER_PASSWORD, (userid,))
            result = cursor.fetchone()
            return result[0] if result else None

    # Get all users
    def get_all_users(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(GET_ALL_USERS)
            return cursor.fetchall()

    # Save a game
    def saveGame(self, firstto, winner, userid):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERT_NEW_GAME, (firstto, winner, userid))
            conn.commit()
            print("Game saved successfully!")

    # Get all games for a user
    def get_user_games(self, userid):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(GET_ALL_GAMES_BY_USER, (userid,))
            return cursor.fetchall()

    # # Get game count for a user
    # def get_game_count_for_user(self, userid):
    #     with self._connect() as conn:
    #         cursor = conn.cursor()
    #         cursor.execute(GET_GAME_COUNT_FOR_USER, (userid,))
    #         return cursor.fetchone()[0]

    # # Get all games where the player won
    # def get_winning_games(self, userid, winner_name):
    #     with self._connect() as conn:
    #         cursor = conn.cursor()
    #         cursor.execute(GET_WINNING_GAMES, (userid, winner_name))
    #         return cursor.fetchall()

    # # Delete a game by ID
    # def delete_game(self, gameid):
    #     with self._connect() as conn:
    #         cursor = conn.cursor()
    #         cursor.execute(DELETE_GAME_BY_ID, (gameid,))
    #         conn.commit()
    #         print(f"Game with ID {gameid} deleted successfully!")
