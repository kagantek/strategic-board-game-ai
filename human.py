#Kagan Tek - 20210702027 - Strategic Board Game With AI

# handles human player moves and validation
class Human:
    def __init__(self, board, game):
        # setup human player
        self.board = board
        self.game = game

    # start human turn
    def play_turn(self):
        self.game.start_human_turn()

    # validate move based on direction
    def validate_move(self, x, y, direction):
        from constants import DIRECTIONS
        if direction not in DIRECTIONS:
            return False
        dx, dy = DIRECTIONS[direction]
        return self.board.is_valid_move(x, y, x + dx, y + dy)

    # execute move based on direction
    def execute_move(self, x, y, direction):
        self.board.move_piece(x, y, direction)

    # validate move based on coordinates
    def validate_move_coords(self, x, y, new_x, new_y):
        return self.board.is_valid_move(x, y, new_x, new_y)

    # execute move based on coordinates
    def execute_move_coords(self, x, y, new_x, new_y):
        self.board.move_piece_by_coords(x, y, new_x, new_y)