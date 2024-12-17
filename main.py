from game import Game
from gui import GameGUI

if __name__ == "__main__":
    game = Game()
    gui = GameGUI(game)
    gui.run()
