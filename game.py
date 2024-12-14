from board import Board
from human import Human
from ai import AI

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = "AI"
        self.total_moves = 0
        self.human_player = Human(self.board, self)
        self.ai_player = AI(self.board, self)

    def play_turn(self):
        self.board.display()
        if self.turn == "AI":
            print("AI's turn...")
            self.ai_player.play_turn()
        else:
            print("Human's turn...")
            self.human_player.play_turn()

        self.switch_turn()
        self.total_moves += 1

    def switch_turn(self):
        self.turn = "Human" if self.turn == "AI" else "AI"

    def is_game_over(self):
        if self.board.triangle == 0 and self.board.circle > 0:
            print("Human wins!")
            return True
        elif self.board.circle == 0 and self.board.triangle > 0:
            print("AI wins!")
            return True
        elif self.board.circle == 0 and self.board.triangle == 0:
            print("It's a draw!")
            return True
        elif self.total_moves >= 50:
            if self.board.triangle > self.board.circle:
                print("AI wins!")
            elif self.board.triangle < self.board.circle:
                print("Human wins!")
            else:
                print("It's a draw!")
            return True
        return False
    
    def return_total_moves(self):
        return self.total_moves

    def run(self):
        print("Welcome to the Strategic Board Game!")
        while not self.is_game_over():
            self.play_turn()
        print("Game Over")
