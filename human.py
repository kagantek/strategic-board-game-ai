class Human:
    def __init__(self, board):
        self.board = board

    def play_turn(self):
        player_pieces = [(x, y) for x in range(self.board.size) for y in range(self.board.size) if self.board.grid[x][y] == 'O']

        for x, y in player_pieces:
            print(f"Current board state:")
            self.board.display()
            print(f"Now moving piece at ({x}, {y})")
            self.move_piece(x, y)

    def move_piece(self, x, y):
        while True:
            try:
                print("Choose the direction to move:")
                print("1. Up\n2. Down\n3. Left\n4. Right")
                choice = input("Enter your choice (1-4): ").strip()

                # Map choice to direction
                direction = self.get_direction(choice)
                if not direction:
                    raise ValueError("Invalid choice. Please select 1, 2, 3, or 4.")

                # Validate the move
                if not self.validate_move(x, y, direction):
                    raise ValueError("Invalid move! The destination is either occupied or out of bounds.")

                # Perform the move
                self.execute_move(x, y, direction)
                print(f"Moved piece at ({x}, {y}) {direction}.")
                break  # Exit loop if the move is successful

            except ValueError as e:
                print(f"Error: {e}. Please try again.")

    def get_direction(self, choice):
        directions = {"1": "up", "2": "down", "3": "left", "4": "right"}
        return directions.get(choice)

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
