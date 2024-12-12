import os
import cv2
from Model.Model import Model

class ModelController:
    def __init__(self):
        self.model = Model()

    def getImages(self):
        ''' Get the images '''
        
        # get the path to the folder containing the images
        image_folder = 'Model/images'
        # print(os.getcwd()) # debug
        image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.jpg')]

        # Load and return the images
        images = []
        for path in image_paths:
            image = cv2.imread(path)
            images.append(image)
        return images
    
    def getRecordedGames(self, username):
        """
        Fetch and format recorded games for a specific user.
        Format the result as a list of strings describing the game outcomes.
        """
        # Fetch the recorded games for the given user (gameid, firstto, winner)
        userid = self.model.get_userid(username)
        games = self.model.get_user_games(userid)

        formatted_games = []
        if games:
            for game in games:
                game_id, firstto, winner = game
                # Format the output based on the winner
                if winner == username:
                    formatted_games.append(f"You Won! You were first to {firstto}")
                elif winner == "Computer":
                    formatted_games.append(f"You Lost :( Computer was first to {firstto}")
            
            return formatted_games
        else:
            print(f"You have not played any games yet.")
            return ["No games played yet."]
    
    def getAllPlayers(self):
        ''' Get all players '''
        # return all players
        users = self.model.get_all_users()
        return [user[1] for user in users]
    
    def getPlayerPassword(self, username):
        ''' Get the player password '''
        userid = self.model.get_userid(username)
        password = self.model.get_user_password(userid)
        # return the player password
        return password
    
    def registerNewPlayer(self, username, password):
        ''' Register a new player '''
        # register the new player
        # add the player to the database
        if self.model.check_user_existence(username):
            print(f"User '{username}' already exists.")
        else:
            self.model.create_user(username, password)
            print(f"User '{username}' registered successfully!")
        return []
    
    def saveGame(self, winning_score, winner, username):
        ''' Save user's game '''
        userid = self.model.get_userid(username)
        self.model.saveGame(winning_score, winner, userid)
        return None