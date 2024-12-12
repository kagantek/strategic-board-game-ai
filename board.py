class Board:
    def __init__(self):
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

    def capture_piece(self, x, y):
        self.grid[x][y] = '.'

    def reset(self):
        self.grid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.initialize_board()



#Test
if __name__ == "__main__":
    board = Board()
    print("Initial Board:")
    board.display()

    print("Move triangle from (0, 0) up (invalid):")
    try:
        board.move_piece(0, 0, "up")
    except ValueError as e:
        print(f"Error: {e}")
    board.display()

    print("Move triangle from (0, 0) right:")
    try:
        board.move_piece(0, 0, "right")
    except ValueError as e:
        print(f"Error: {e}")
    board.display()

    print("Move triangle from (0, 1) down:")
    try:
        board.move_piece(0, 1, "down")
    except ValueError as e:
        print(f"Error: {e}")
    board.display()

    print("Captured piece (6,0): ")
    board.capture_piece(6, 0)
    board.display()

    print("Resetting the board:")
    board.reset()
    board.display()
