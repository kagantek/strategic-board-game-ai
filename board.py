class Board:
    def __init__(self):
        self.triangle = 4
        self.circle = 4
        self.size = 7
        self.grid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.initialize_board()

    def initialize_board(self):
        #Triangle (Player 1 - AI)
        self.grid[0][0] = 'T'
        self.grid[2][0] = 'T'
        self.grid[4][6] = 'T'
        self.grid[6][6] = 'T'

        # Circle (Player 2 - Human)
        self.grid[4][0] = 'O'
        self.grid[6][0] = 'O'
        self.grid[0][6] = 'O'
        self.grid[2][6] = 'O'

    def display(self):
        print("  " + " ".join(str(i) for i in range(self.size)))
        for idx, row in enumerate(self.grid):
            print(f"{idx} " + " ".join(row))
        print()

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
            raise ValueError("Invalid direction. Use 'up', 'down', 'left', or 'right'.")
        
        if not self.is_valid_move(x, y, new_x, new_y):
            raise ValueError(f"Invalid move from ({x}, {y}) to ({new_x}, {new_y}).")

        self.grid[new_x][new_y] = self.grid[x][y]
        self.grid[x][y] = '.'

        self.check_captures()

    def capture_piece(self, x, y):
        if(self.grid[x][y] == 'T'):
            self.triangle -= 1
        elif(self.grid[x][y] == 'O'):
            self.circle -= 1
        
        self.grid[x][y] = '.'

    def check_captures(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

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


    def reset(self):
        self.grid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.initialize_board()



#Test
if __name__ == "__main__":
    board = Board()
    print("Initial Board:")
    board.display()

    print("Simulate a multiple capture scenario (TOOT):")
    board.grid[2][0] = 'T'
    board.grid[2][1] = 'O'
    board.grid[2][2] = 'O'
    board.grid[2][3] = 'T'
    board.display()

    print("Check for captures:")
    board.check_captures()
    board.display()

    print("Remaining pieces - Triangles:", board.triangle, "Circles:", board.circle)
