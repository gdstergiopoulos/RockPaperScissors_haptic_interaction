import requests
class DeviceController:
    def __init__(self):
        pass

    def sendWinnerMessage(self):
        ''' Send a message to the winner '''
        requests.get("https://maker.ifttt.com/trigger/win/with/key/pM1ozEUO5xiOUE5_g0RXgILQN8aLT3kw2KpVtTp-LRg")
        return None
    
    def sendLoserMessage(self):
        ''' Send a message to the loser '''
        requests.get("https://maker.ifttt.com/trigger/loss/with/key/pM1ozEUO5xiOUE5_g0RXgILQN8aLT3kw2KpVtTp-LRg")
        return None
