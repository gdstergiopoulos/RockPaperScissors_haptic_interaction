# queries.py
# SQL queries for the Rock Paper Scissors Game

# Query to retrieve all users
GET_ALL_USERS = """
SELECT userid, username
FROM User;
"""

# Query to retrieve a user's password by username
GET_USER_PASSWORD = """
SELECT password
FROM User
WHERE userid = ?;
"""

# Query to retrieve a user's id
GET_USER_ID = """
SELECT userid
FROM User
WHERE username = ?
"""

# Query to create a new user
INSERT_NEW_USER = """
INSERT INTO User (username, password)
VALUES (?, ?);
"""

# Query to check if a user exists
CHECK_USER_EXISTENCE = """
SELECT userid
FROM User
WHERE username = ?;
"""

# Query to retrieve all game records for a user
GET_ALL_GAMES_BY_USER = """
SELECT gameid, firstto, winner
FROM Game
WHERE userid = ?;
"""

# Query to insert a new game record
INSERT_NEW_GAME = """
INSERT INTO Game (firstto, winner, userid)
VALUES (?, ?, ?);
"""

# # Query to get the count of games a user has played
# GET_GAME_COUNT_FOR_USER = """
# SELECT COUNT(*)
# FROM Game
# WHERE userid = ?;
# """

# # Query to get all games where the player has won
# GET_WINNING_GAMES = """
# SELECT gameid, rounds, winner
# FROM Game
# WHERE userid = ? AND winner = ?;
# """

# # Query to delete a specific game record
# DELETE_GAME_BY_ID = """
# DELETE FROM Game
# WHERE gameid = ?;
# """
