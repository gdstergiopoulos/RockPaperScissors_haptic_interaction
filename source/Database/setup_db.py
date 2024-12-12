import sqlite3

def setup_database():
    # Connect to the SQLite3 database (it creates the file if it doesn't exist)
    conn = sqlite3.connect('Database/rps_game.db')
    cursor = conn.cursor()
    
    # SQL statements to create tables
    user_table = '''
    CREATE TABLE IF NOT EXISTS User (
        userid INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    '''
    
    game_table = '''
    CREATE TABLE IF NOT EXISTS Game (
        gameid INTEGER PRIMARY KEY AUTOINCREMENT,
        firstto INTEGER NOT NULL,
        winner TEXT,
        userid INTEGER NOT NULL,
        FOREIGN KEY (userid) REFERENCES User(userid)
    );
    '''
    
    # Execute table creation
    cursor.execute(user_table)
    cursor.execute(game_table)
    
    print("Database setup complete. Tables created successfully.")
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
