
from Controller.mainController import MainController

def main():
    app = MainController()
    app.run()
    app.on_exit()

if __name__ == '__main__':
    main()