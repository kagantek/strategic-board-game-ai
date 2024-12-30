#Kagan Tek - 20210702027 - Strategic Board Game With AI

# main game logic, handles turns and game flow
from board import Board
from human import Human
from ai import AI
from constants import DIRECTIONS

class Game:
    def __init__(self):
        # setup game components
        self.board = Board()
        self.turn = "AI"
        self.total_moves = 0
        self.human_player = Human(self.board, self)
        self.ai_player = AI(self.board, self)
        self.gui = None

        self.human_pieces_to_move = []
        self.current_piece_index = 0
        self.selected_piece = None
        self.moved_pieces = set()  # Track pieces moved this turn

    def set_gui(self, gui):
        self.gui = gui

    def run(self):
        self.gui.update_board_display()
        self.play_turn()

    def play_turn(self):
        if self.is_game_over():
            return
        if self.turn == "AI":
            self.gui.set_info("AI's turn... thinking.")
            self.gui.root.after(500, self.ai_action)
        else:
            self.gui.set_info("Human's turn")
            self.human_player.play_turn()

    def ai_action(self):
        self.ai_player.play_turn()
        self.gui.update_board_display()
        self.switch_turn()
        self.total_moves += 1
        if not self.is_game_over():
            self.play_turn()

    def start_human_turn(self):
        self.moved_pieces.clear()  # Reset moved pieces at turn start
        self.available_pieces = [(x, y) for x in range(self.board.size) 
                        for y in range(self.board.size) 
                        if self.board.grid[x][y] == 'O']
        self.gui.moves_remaining = 2
        self.gui.set_info("Select a piece to move. Moves remaining: 2")
        self.gui.enable_piece_selection(self.available_pieces)

    def after_human_piece_moved(self):
        self.selected_piece = None
        self.gui.update_board_display()
        self.moves_remaining -= 1
        
        if self.moves_remaining > 0:
            self.gui.set_info(f"Select another piece. Moves remaining: {self.moves_remaining}")
        else:
            self.end_human_turn()

    def move_next_human_piece(self):
        if self.current_piece_index >= len(self.human_pieces_to_move):
            self.end_human_turn()
            return
        piece_pos = self.human_pieces_to_move[self.current_piece_index]
        x, y = piece_pos
        self.selected_piece = (x, y)
        self.gui.update_board_display()
        self.gui.set_info(f"Move piece at ({x}, {y}). Select it or use directions.")
        self.gui.enable_direction_buttons()

    def execute_human_move_direction(self, direction):
        if not self.selected_piece:
            self.gui.error("No piece selected.")
            return
        x, y = self.selected_piece
        if not self.human_player.validate_move(x, y, direction):
            self.gui.error("Invalid Move: You cannot move in that direction.")
            return
        self.human_player.execute_move(x, y, direction)
        self.after_human_piece_moved()

    def execute_human_move_coords(self, x, y):
        if not self.gui.selected_piece:
            self.gui.error("No piece selected.")
            return
        sx, sy = self.gui.selected_piece
        
        # Check if piece was already moved
        if (sx, sy) in self.moved_pieces:
            self.gui.error("This piece was already moved.")
            return
            
        if not self.human_player.validate_move_coords(sx, sy, x, y):
            self.gui.error("Invalid Move: Cannot move to that cell.")
            return
            
        self.human_player.execute_move_coords(sx, sy, x, y)
        self.moved_pieces.add((x, y))  # Track moved piece
        self.gui.disable_direction_buttons()
        self.gui.update_board_display()

        # Check for immediate game over
        if self.board.triangle == 0:
            self.gui.game_over("Human wins!")
            return

        # Check if any valid moves remain
        if not self._has_valid_moves('O'):
            self.moves_remaining = 0
            self.gui.moves_remaining = 0
            self.end_human_turn()
            return

        if self.gui.moves_remaining > 1:
            self.gui.set_info(f"Select another piece. Moves remaining: {self.gui.moves_remaining - 1}")

    def after_human_piece_moved(self):
        self.selected_piece = None
        self.gui.update_board_display()
        self.current_piece_index += 1
        self.move_next_human_piece()

    def end_human_turn(self):
        self.gui.disable_direction_buttons()
        self.switch_turn()
        self.total_moves += 1
        if not self.is_game_over():
            self.play_turn()

    def switch_turn(self):
        self.turn = "Human" if self.turn == "AI" else "AI"

    def is_game_over(self):
        if self.board.triangle == 0 and self.board.circle > 0:
            self.gui.game_over("Human wins!")
            return True
        elif self.board.circle == 0 and self.board.triangle > 0:
            self.gui.game_over("AI wins!")
            return True
        elif self.board.circle == 0 and self.board.triangle == 0:
            self.gui.game_over("It's a draw!")
            return True
        elif self.total_moves >= 50:
            if self.board.triangle > self.board.circle:
                self.gui.game_over("AI wins!")
            elif self.board.triangle < self.board.circle:
                self.gui.game_over("Human wins!")
            else:
                self.gui.game_over("It's a draw!")
            return True
        return False

    def return_total_moves(self):
        return self.total_moves

    def _has_valid_moves(self, piece_type):
        # Check if any unmoved pieces can make valid moves
        for x in range(self.board.size):
            for y in range(self.board.size):
                if (self.board.grid[x][y] == piece_type and 
                    (x, y) not in self.moved_pieces):
                    # Check all possible directions
                    for dx, dy in DIRECTIONS.values():
                        new_x, new_y = x + dx, y + dy
                        if (0 <= new_x < self.board.size and 
                            0 <= new_y < self.board.size and 
                            self.board.grid[new_x][new_y] == '.'):
                            return True
        return False