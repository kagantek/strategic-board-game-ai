class AI:
    def __init__(self, board, game, max_depth=3):
        self.board = board
        self.game = game
        self.max_depth = max_depth

    def play_turn(self):
        ai_pieces = [(x, y) for x in range(self.board.size) for y in range(self.board.size) if self.board.grid[x][y] == 'T']
        for x, y in ai_pieces:
            best_move = self.find_best_move_for_piece(x, y)
            if best_move:
                direction = best_move
                self.board.move_piece(x, y, direction)

    def find_best_move_for_piece(self, x, y):
        best_score = float('-inf')
        best_direction = None
        for direction in ["up", "down", "left", "right"]:
            if self.validate_move(x, y, direction):
                original_board = [row[:] for row in self.board.grid]
                original_triangle = self.board.triangle
                original_circle = self.board.circle

                self.board.move_piece(x, y, direction)
                score = self.minimax(depth=self.max_depth, is_maximizing=False)

                self.board.grid = original_board
                self.board.triangle = original_triangle
                self.board.circle = original_circle

                if score > best_score:
                    best_score = score
                    best_direction = direction
        return best_direction

    def minimax(self, depth, is_maximizing):
        if depth == 0 or self.is_terminal():
            return self.evaluate_board()

        if is_maximizing:
            max_eval = float('-inf')
            ai_pieces = [(x, y) for x in range(self.board.size) for y in range(self.board.size) if self.board.grid[x][y] == 'T']
            for x, y in ai_pieces:
                for direction in ["up", "down", "left", "right"]:
                    if self.validate_move(x, y, direction):
                        original_board = [row[:] for row in self.board.grid]
                        original_triangle = self.board.triangle
                        original_circle = self.board.circle

                        self.board.move_piece(x, y, direction)
                        eval_ = self.minimax(depth - 1, False)
                        self.board.grid = original_board
                        self.board.triangle = original_triangle
                        self.board.circle = original_circle
                        max_eval = max(max_eval, eval_)
            return max_eval
        else:
            min_eval = float('inf')
            human_pieces = [(x, y) for x in range(self.board.size) for y in range(self.board.size) if self.board.grid[x][y] == 'O']
            for x, y in human_pieces:
                for direction in ["up", "down", "left", "right"]:
                    if self.validate_move(x, y, direction):
                        original_board = [row[:] for row in self.board.grid]
                        original_triangle = self.board.triangle
                        original_circle = self.board.circle

                        self.board.move_piece(x, y, direction)
                        eval_ = self.minimax(depth - 1, True)
                        self.board.grid = original_board
                        self.board.triangle = original_triangle
                        self.board.circle = original_circle
                        min_eval = min(min_eval, eval_)
            return min_eval

    def evaluate_board(self):
        piece_difference = self.board.triangle - self.board.circle
        moves_remaining = 50 - self.game.return_total_moves()
        if moves_remaining > 0:
            return piece_difference + moves_remaining * 0.1
        else:
            return piece_difference

    def is_terminal(self):
        return self.board.triangle == 0 or self.board.circle == 0 or (self.board.triangle + self.board.circle == 0)

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
