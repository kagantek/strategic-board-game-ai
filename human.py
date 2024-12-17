class Human:
    def __init__(self, board, game):
        self.board = board
        self.game = game

    def play_turn(self):
        # Just notify the game that we start human turn, no I/O here
        self.game.start_human_turn()

    def validate_move(self, x, y, direction):
        if direction == "up":
            new_x, new_y = x - 1, y
        elif direction == "down":
            new_x, new_y = x + 1, y
        elif direction == "left":
            new_x, new_y = x, y - 1
        elif direction == "right":
            new_x, new_y = x, y + 1
        else:
            return False
        return self.board.is_valid_move(x, y, new_x, new_y)

    def execute_move(self, x, y, direction):
        self.board.move_piece(x, y, direction)

    def validate_move_coords(self, x, y, new_x, new_y):
        return self.board.is_valid_move(x, y, new_x, new_y)

    def execute_move_coords(self, x, y, new_x, new_y):
        self.board.move_piece_by_coords(x, y, new_x, new_y)
