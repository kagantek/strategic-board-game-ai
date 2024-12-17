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

    def minimax(self, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
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
                        
                        eval_ = self.minimax(depth - 1, False, alpha, beta)
                        
                        self.board.grid = original_board
                        self.board.triangle = original_triangle
                        self.board.circle = original_circle

                        max_eval = max(max_eval, eval_)
                        alpha = max(alpha, eval_)

                        if beta <= alpha:
                            return max_eval
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
                        
                        eval_ = self.minimax(depth - 1, True, alpha, beta)
                        
                        self.board.grid = original_board
                        self.board.triangle = original_triangle
                        self.board.circle = original_circle

                        min_eval = min(min_eval, eval_)
                        beta = min(beta, eval_)

                        if beta <= alpha:
                            return min_eval
            return min_eval


    def evaluate_board(self):
        piece_difference = self.board.triangle - self.board.circle

        ai_mobility = self.calculate_mobility('T')
        human_mobility = self.calculate_mobility('O')
        mobility_score = ai_mobility - human_mobility

        ai_position_score = self.calculate_positional_advantage('T')
        human_position_score = self.calculate_positional_advantage('O')
        positional_advantage = ai_position_score - human_position_score

        ai_capturable = self.calculate_capturable_pieces('T')
        human_capturable = self.calculate_capturable_pieces('O')
        capturing_potential = human_capturable - ai_capturable

        moves_remaining = 50 - self.game.return_total_moves()
        endgame_bonus = moves_remaining * 0.1 if moves_remaining > 0 else 0

        return (
            piece_difference * 1.0 +
            mobility_score * 0.5 +
            positional_advantage * 0.7 +
            capturing_potential * 1.5 +
            endgame_bonus
        )


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
    
    def calculate_mobility(self, player_piece):
        mobility = 0
        directions = ["up", "down", "left", "right"]

        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.board.grid[x][y] == player_piece:
                    for direction in directions:
                        if self.validate_move(x, y, direction):
                            mobility += 1
        return mobility
    
    def calculate_positional_advantage(self, player_piece):
        position_weights = [
            [1, 2, 3, 3, 3, 2, 1],
            [2, 3, 4, 4, 4, 3, 2],
            [3, 4, 5, 5, 5, 4, 3],
            [3, 4, 5, 6, 5, 4, 3],
            [3, 4, 5, 5, 5, 4, 3],
            [2, 3, 4, 4, 4, 3, 2],
            [1, 2, 3, 3, 3, 2, 1],
        ]

        score = 0
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.board.grid[x][y] == player_piece:
                    score += position_weights[x][y]
        return score
    
    def calculate_capturable_pieces(self, player_piece):
        opponent_piece = 'T' if player_piece == 'O' else 'O'
        capturable = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.board.grid[x][y] == player_piece:
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if self.board.is_valid_position(nx, ny) and self.board.grid[nx][ny] == opponent_piece:
                            further_x, further_y = nx + dx, ny + dy
                            if self.board.is_valid_position(further_x, further_y) and self.board.grid[further_x][further_y] == player_piece:
                                capturable += 1
        return capturable


