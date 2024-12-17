class Human:
    def __init__(self, board, game):
        self.board = board
        self.game = game

    def play_turn(self):
        self.game.start_human_turn()

    def validate_move(self, x, y, direction):
        from constants import DIRECTIONS
        if direction not in DIRECTIONS:
            return False
        dx, dy = DIRECTIONS[direction]
        return self.board.is_valid_move(x, y, x + dx, y + dy)

    def execute_move(self, x, y, direction):
        self.board.move_piece(x, y, direction)

    def validate_move_coords(self, x, y, new_x, new_y):
        return self.board.is_valid_move(x, y, new_x, new_y)

    def execute_move_coords(self, x, y, new_x, new_y):
        self.board.move_piece_by_coords(x, y, new_x, new_y)