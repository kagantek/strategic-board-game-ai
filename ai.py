from constants import DIRECTIONS

class AI:
    def __init__(self, board, game, max_depth=3):
        self.board = board
        self.game = game
        self.max_depth = max_depth

    def play_turn(self):
        ai_pieces = [(x, y) for x in range(self.board.size) for y in range(self.board.size) if self.board.grid[x][y] == 'T']
        moves_made = 0
        while moves_made < 2 and ai_pieces:
            best_score = float('-inf')
            best_move = None
            best_piece = None
            
            for x, y in ai_pieces:
                direction = self.find_best_move_for_piece(x, y)
                if direction:
                    original_state = self.snapshot_board()
                    self.board.move_piece(x, y, direction)
                    score = self.evaluate_board()
                    self.restore_board(original_state)
                    
                    if score > best_score:
                        best_score = score
                        best_move = direction
                        best_piece = (x, y)
            
            if best_piece and best_move:
                self.board.move_piece(best_piece[0], best_piece[1], best_move)
                ai_pieces.remove(best_piece)
                moves_made += 1
            else:
                break

    def find_best_move_for_piece(self, x, y):
        best_score = float('-inf')
        best_direction = None
        for direction, (dx, dy) in DIRECTIONS.items():
            if self.board.is_valid_move(x, y, x + dx, y + dy):
                original_state = self.snapshot_board()
                self.board.move_piece(x, y, direction)
                score = self.minimax(self.max_depth, is_maximizing=False)
                self.restore_board(original_state)

                if score > best_score:
                    best_score = score
                    best_direction = direction

        return best_direction

    def snapshot_board(self):
        return {
            'grid': [row[:] for row in self.board.grid],
            'triangle': self.board.triangle,
            'circle': self.board.circle
        }

    def restore_board(self, state):
        self.board.grid = state['grid']
        self.board.triangle = state['triangle']
        self.board.circle = state['circle']

    def minimax(self, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or self.is_terminal():
            return self.evaluate_board()

        if is_maximizing:
            return self.maximize(depth, alpha, beta)
        else:
            return self.minimize(depth, alpha, beta)

    def maximize(self, depth, alpha, beta):
        max_eval = float('-inf')
        ai_pieces = [(x, y) for x in range(self.board.size) for y in range(self.board.size) if self.board.grid[x][y] == 'T']
        for x, y in ai_pieces:
            for direction, (dx, dy) in DIRECTIONS.items():
                if self.board.is_valid_move(x, y, x + dx, y + dy):
                    original_state = self.snapshot_board()
                    self.board.move_piece(x, y, direction)

                    eval_ = self.minimax(depth - 1, False, alpha, beta)

                    self.restore_board(original_state)
                    max_eval = max(max_eval, eval_)
                    alpha = max(alpha, eval_)
                    if beta <= alpha:
                        return max_eval
        return max_eval

    def minimize(self, depth, alpha, beta):
        min_eval = float('inf')
        human_pieces = [(x, y) for x in range(self.board.size) for y in range(self.board.size) if self.board.grid[x][y] == 'O']
        for x, y in human_pieces:
            for direction, (dx, dy) in DIRECTIONS.items():
                if self.board.is_valid_move(x, y, x + dx, y + dy):
                    original_state = self.snapshot_board()
                    self.board.move_piece(x, y, direction)

                    eval_ = self.minimax(depth - 1, True, alpha, beta)

                    self.restore_board(original_state)
                    min_eval = min(min_eval, eval_)
                    beta = min(beta, eval_)
                    if beta <= alpha:
                        return min_eval
        return min_eval

    def evaluate_board(self):
        piece_diff = self.board.triangle - self.board.circle
        ai_mobility = self.calculate_mobility('T')
        human_mobility = self.calculate_mobility('O')
        mobility_score = ai_mobility - human_mobility

        ai_pos_score = self.calculate_positional_advantage('T')
        human_pos_score = self.calculate_positional_advantage('O')
        positional_advantage = ai_pos_score - human_pos_score

        ai_capturable = self.calculate_capturable_pieces('T')
        human_capturable = self.calculate_capturable_pieces('O')
        capturing_potential = human_capturable - ai_capturable

        moves_remaining = 50 - self.game.return_total_moves()
        endgame_bonus = moves_remaining * 0.1 if moves_remaining > 0 else 0

        return (
            piece_diff * 1.0 +
            mobility_score * 0.5 +
            positional_advantage * 0.7 +
            capturing_potential * 1.5 +
            endgame_bonus
        )

    def is_terminal(self):
        return self.board.triangle == 0 or self.board.circle == 0 or (self.board.triangle + self.board.circle == 0)

    def calculate_mobility(self, piece):
        mobility = 0
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.board.grid[x][y] == piece:
                    for dx, dy in DIRECTIONS.values():
                        if self.board.is_valid_move(x, y, x + dx, y + dy):
                            mobility += 1
        return mobility

    def calculate_positional_advantage(self, piece):
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
                if self.board.grid[x][y] == piece:
                    score += position_weights[x][y]
        return score

    def calculate_capturable_pieces(self, piece):
        opponent = 'T' if piece == 'O' else 'O'
        capturable = 0
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.board.grid[x][y] == piece:
                    for dx, dy in DIRECTIONS.values():
                        nx, ny = x + dx, y + dy
                        if self.board.is_valid_position(nx, ny) and self.board.grid[nx][ny] == opponent:
                            fx, fy = nx + dx, ny + dy
                            if self.board.is_valid_position(fx, fy) and self.board.grid[fx][fy] == piece:
                                capturable += 1
        return capturable