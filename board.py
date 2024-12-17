class Board:
    def __init__(self):
        self.triangle = 4
        self.circle = 4
        self.size = 7
        self.grid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.initialize_board()

    def initialize_board(self):
        self.grid[0][0] = 'T'
        self.grid[2][0] = 'T'
        self.grid[4][6] = 'T'
        self.grid[6][6] = 'T'

        self.grid[4][0] = 'O'
        self.grid[6][0] = 'O'
        self.grid[0][6] = 'O'
        self.grid[2][6] = 'O'

    def is_valid_position(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def is_valid_move(self, x, y, new_x, new_y):
        if not self.is_valid_position(x, y) or not self.is_valid_position(new_x, new_y):
            return False
        if self.grid[x][y] == '.':
            return False
        if self.grid[new_x][new_y] != '.':
            return False
        return True

    def move_piece(self, x, y, direction):
        if direction == "up":
            new_x, new_y = x - 1, y
        elif direction == "down":
            new_x, new_y = x + 1, y
        elif direction == "left":
            new_x, new_y = x, y - 1
        elif direction == "right":
            new_x, new_y = x, y + 1
        else:
            raise ValueError("Invalid direction")

        if not self.is_valid_move(x, y, new_x, new_y):
            raise ValueError(f"Invalid move from ({x}, {y}) to ({new_x}, {new_y}).")

        self.grid[new_x][new_y] = self.grid[x][y]
        self.grid[x][y] = '.'
        self.check_captures()

    def move_piece_by_coords(self, x, y, new_x, new_y):
        if abs(x - new_x) + abs(y - new_y) != 1:
            raise ValueError("Invalid move coordinates.")
        if not self.is_valid_move(x, y, new_x, new_y):
            raise ValueError("Invalid move by coordinates.")
        self.grid[new_x][new_y] = self.grid[x][y]
        self.grid[x][y] = '.'
        self.check_captures()

    def capture_piece(self, x, y):
        if self.grid[x][y] == 'T':
            self.triangle -= 1
        elif self.grid[x][y] == 'O':
            self.circle -= 1
        self.grid[x][y] = '.'

    def check_captures(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        to_capture = []
        for x in range(self.size):
            for y in range(self.size):
                piece = self.grid[x][y]
                if piece == '.':
                    continue
                opponent = 'T' if piece == 'O' else 'O'
                for dx, dy in directions:
                    captured_pieces = []
                    nx, ny = x + dx, y + dy
                    while self.is_valid_position(nx, ny) and self.grid[nx][ny] == opponent:
                        captured_pieces.append((nx, ny))
                        nx, ny = nx + dx, ny + dy

                    if self.is_valid_position(nx, ny) and self.grid[nx][ny] == piece:
                        to_capture.extend(captured_pieces)
                    elif not self.is_valid_position(nx, ny):
                        to_capture.extend(captured_pieces)
        for cx, cy in to_capture:
            self.capture_piece(cx, cy)
