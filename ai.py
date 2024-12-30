from constants import DIRECTIONS

class AI:
    def __init__(self, board, game, max_depth=4):
        self.board = board
        self.game = game
        self.max_depth = max_depth
        self.weights = self._initialize_weights()

    def play_turn(self):
        ai_pieces = [(x, y) for x in range(self.board.size) 
                     for y in range(self.board.size) 
                     if self.board.grid[x][y] == 'T']
                     
        moves_made = 0
        moved_pieces = set()

        while moves_made < 2 and ai_pieces:
            available_pieces = [p for p in ai_pieces if p not in moved_pieces]
            if not available_pieces:
                break

            move = self._find_best_move(available_pieces)
            if move:
                piece, direction = move
                self._execute_move(piece, direction, moved_pieces)
                moves_made += 1
            else:
                break

    def _find_best_move(self, pieces):
        best_score = float('-inf')
        best_move = None

        for piece in pieces:
            for direction in DIRECTIONS:
                if self._is_valid_move(piece, direction):
                    score = self._evaluate_move(piece, direction)
                    if score > best_score:
                        best_score = score
                        best_move = (piece, direction)

        return best_move

    def _evaluate_board(self):
        weights = self._get_phase_weights()
        
        scores = {
            'pieces': self._evaluate_pieces() * weights['pieces'],
            'position': self._evaluate_position() * weights['position'],
            'mobility': self._evaluate_mobility() * weights['mobility'],
            'threats': self._evaluate_threats() * weights['threats']
        }
        
        return sum(scores.values())

    def _initialize_weights(self):
        return {
            'early_game': {
                'pieces': 100,
                'position': 90,
                'mobility': 80,
                'threats': 70,
                # Add missing keys
                'piece_value': 100,
                'capture_potential': 70,
                'defense': 50
            },
            'mid_game': {
                'pieces': 90,
                'position': 80,
                'mobility': 85,
                'threats': 100,
                # Add missing keys
                'piece_value': 90,
                'capture_potential': 100,
                'defense': 60
            },
            'late_game': {
                'pieces': 120,
                'position': 60,
                'mobility': 70,
                'threats': 110,
                # Add missing keys
                'piece_value': 120,
                'capture_potential': 110,
                'defense': 80
            }
        }

    def _get_phase_weights(self, total_moves):
        if total_moves < 15:
            return self.weights['early_game']
        elif total_moves < 35:
            return self.weights['mid_game']
        else:
            return self.weights['late_game']

    def _evaluate_pieces(self):
        piece_diff = self.board.triangle - self.board.circle
        remaining_pieces = self.board.triangle + self.board.circle
        if remaining_pieces <= 4:
            return piece_diff * 1.5
        return piece_diff

    def _evaluate_position(self):
        position_weights = [
            [3, 4, 5, 5, 5, 4, 3],
            [4, 6, 7, 7, 7, 6, 4],
            [5, 7, 8, 8, 8, 7, 5],
            [5, 7, 8, 9, 8, 7, 5],
            [5, 7, 8, 8, 8, 7, 5],
            [4, 6, 7, 7, 7, 6, 4],
            [3, 4, 5, 5, 5, 4, 3]
        ]
        
        ai_pos_score = 0
        human_pos_score = 0
        
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.board.grid[x][y] == 'T':
                    ai_pos_score += position_weights[x][y]
                elif self.board.grid[x][y] == 'O':
                    human_pos_score += position_weights[x][y]
        
        return ai_pos_score - human_pos_score

    def _evaluate_mobility(self):
        ai_mobility = self.calculate_mobility('T')
        human_mobility = self.calculate_mobility('O')
        
        if ai_mobility == 0:
            return -1000
        if human_mobility == 0:
            return 1000
            
        return (ai_mobility - human_mobility) * 0.8

    def _evaluate_threats(self):
        ai_threats = self._count_capture_threats('T')
        human_threats = self._count_capture_threats('O')
        
        immediate_capture_weight = 2.0
        potential_capture_weight = 1.0
        
        return ((ai_threats['immediate'] * immediate_capture_weight) -
                (human_threats['immediate'] * immediate_capture_weight) +
                (ai_threats['potential'] * potential_capture_weight) -
                (human_threats['potential'] * potential_capture_weight))

    def _count_capture_threats(self, piece):
        opponent = 'O' if piece == 'T' else 'T'
        threats = {'immediate': 0, 'potential': 0}
        
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.board.grid[x][y] == piece:
                    for dx, dy in DIRECTIONS.values():
                        if self._is_capture_threat(x, y, dx, dy, opponent):
                            threats['immediate'] += 1
                        if self._is_potential_threat(x, y, dx, dy, opponent):
                            threats['potential'] += 1
        
        return threats

    def _is_capture_threat(self, x, y, dx, dy, opponent):
        nx, ny = x + dx, y + dy
        if self.board.is_valid_position(nx, ny) and self.board.grid[nx][ny] == opponent:
            fx, fy = nx + dx, ny + dy
            if self.board.is_valid_position(fx, fy) and self.board.grid[fx][fy] == self.board.grid[x][y]:
                return True
        return False

    def _is_potential_threat(self, x, y, dx, dy, opponent):
        nx, ny = x + dx, y + dy
        if self.board.is_valid_position(nx, ny) and self.board.grid[nx][ny] == opponent:
            fx, fy = nx + dx, ny + dy
            if self.board.is_valid_position(fx, fy) and self.board.grid[fx][fy] == '.':
                return True
        return False

    def calculate_mobility(self, piece):
        mobility = 0
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.board.grid[x][y] == piece:
                    for dx, dy in DIRECTIONS.values():
                        if self.board.is_valid_move(x, y, x + dx, y + dy):
                            mobility += 1
        return mobility

    def _execute_move(self, piece, direction, moved_pieces):
        x, y = piece
        new_x = x + DIRECTIONS[direction][0]
        new_y = y + DIRECTIONS[direction][1]
        self.board.move_piece(x, y, direction)
        moved_pieces.add((new_x, new_y))
        self.board.grid[x][y] = '.'
        self.board.grid[new_x][new_y] = 'T'

    def _is_valid_move(self, piece, direction):
        x, y = piece
        dx, dy = DIRECTIONS[direction]
        return self.board.is_valid_move(x, y, x + dx, y + dy)

    def _evaluate_move(self, piece, direction):
        x, y = piece
        dx, dy = DIRECTIONS[direction]
        original_state = self.snapshot_board()
        self.board.move_piece(x, y, direction)
        score = self.evaluate_board()
        self.restore_board(original_state)
        return score

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

    def evaluate_board(self):
        total_moves = self.game.return_total_moves()
        weights = self._get_phase_weights(total_moves)
        
        piece_score = self._evaluate_piece_count() * weights['piece_value']
        mobility_score = self._evaluate_mobility() * weights['mobility']
        position_score = self._evaluate_position() * weights['position']
        capture_score = self._evaluate_capture_potential() * weights['capture_potential']
        defense_score = self._evaluate_defense() * weights['defense']
        
        pattern_score = self._evaluate_patterns() * 50
        control_score = self._evaluate_board_control() * 40
        
        total_score = (piece_score + mobility_score + position_score + 
                      capture_score + defense_score + pattern_score + 
                      control_score)
        
        return total_score

    def _evaluate_piece_count(self):
        piece_diff = self.board.triangle - self.board.circle
        remaining_pieces = self.board.triangle + self.board.circle
        
        if remaining_pieces <= 4:
            return piece_diff * 1.5
        return piece_diff

    def _evaluate_capture_potential(self):
        ai_threats = self._count_capture_threats('T')
        human_threats = self._count_capture_threats('O')
        
        immediate_capture_weight = 2.0
        potential_capture_weight = 1.0
        
        return ((ai_threats['immediate'] * immediate_capture_weight) -
                (human_threats['immediate'] * immediate_capture_weight) +
                (ai_threats['potential'] * potential_capture_weight) -
                (human_threats['potential'] * potential_capture_weight))

    def _evaluate_defense(self):
        ai_vulnerable = self._count_vulnerable_pieces('T')
        human_vulnerable = self._count_vulnerable_pieces('O')
        
        if self.game.return_total_moves() > 35:
            return (human_vulnerable - ai_vulnerable) * 1.5
        return human_vulnerable - ai_vulnerable

    def _evaluate_patterns(self):
        score = 0
        score += self._evaluate_center_control('T') - self._evaluate_center_control('O')
        score += self._evaluate_edges('T') - self._evaluate_edges('O')
        return score

    def _evaluate_center_control(self, piece):
        center_score = 0
        center_squares = [(3,3), (3,4), (4,3), (4,4)]
        for x, y in center_squares:
            if self.board.grid[x][y] == piece:
                center_score += 2
        return center_score

    def _evaluate_edges(self, piece):
        edge_score = 0
        edges = [(0,i) for i in range(self.board.size)]
        edges += [(i,0) for i in range(self.board.size)]
        edges += [(self.board.size-1,i) for i in range(self.board.size)]
        edges += [(i,self.board.size-1) for i in range(self.board.size)]
        
        for x, y in edges:
            if self.board.grid[x][y] == piece:
                edge_score += 1
        return edge_score

    def _evaluate_board_control(self):
        return 0

    def _count_vulnerable_pieces(self, piece):
        opponent = 'O' if piece == 'T' else 'T'
        vulnerable = 0
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.board.grid[x][y] == piece:
                    for dx, dy in DIRECTIONS.values():
                        if self._is_capture_threat(x, y, dx, dy, opponent):
                            vulnerable += 1
        return vulnerable

    def is_terminal(self):
        return self.board.triangle == 0 or self.board.circle == 0 or (self.board.triangle + self.board.circle == 0)

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
