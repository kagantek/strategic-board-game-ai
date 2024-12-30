#Kagan Tek - 20210702027 - Strategic Board Game With AI

from game import Game
from gui import GameGUI

if __name__ == "__main__":
    game = Game()
    gui = GameGUI(game)
    gui.run()
