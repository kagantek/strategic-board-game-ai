import tkinter as tk
from tkinter import messagebox

class GameGUI:
    def __init__(self, game):
        self.game = game
        self.game.set_gui(self)

        self.root = tk.Tk()
        self.root.title("Strategic Board Game")
        self.root.geometry("900x700")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)

        self.cells = []
        cell_font = ("Arial", 16)
        size = self.game.board.size
        for i in range(size + 1):
            row_cells = []
            for j in range(size + 1):
                if i == 0 and j == 0:
                    lbl = tk.Label(self.main_frame, width=3, height=1, font=cell_font, borderwidth=2, relief="groove", bg="lightgray", text="")
                elif i == 0:
                    lbl = tk.Label(self.main_frame, width=3, height=1, font=cell_font, borderwidth=2, relief="groove", bg="lightgray", text=str(j-1))
                elif j == 0:
                    lbl = tk.Label(self.main_frame, width=3, height=1, font=cell_font, borderwidth=2, relief="groove", bg="lightgray", text=str(i-1))
                else:
                    lbl = tk.Label(self.main_frame, width=3, height=1, font=cell_font, borderwidth=2, relief="groove")
                    lbl.bind("<Button-1>", lambda e, x=i-1, y=j-1: self.on_cell_click(x, y))
                lbl.grid(row=i, column=j)
                row_cells.append(lbl)
            self.cells.append(row_cells)

        self.info_label = tk.Label(self.root, text="Welcome!")
        self.info_label.pack()

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack()

        self.up_button = tk.Button(self.buttons_frame, text="Up", command=lambda: self.game.execute_human_move_direction("up"))
        self.up_button.grid(row=0, column=1)
        self.left_button = tk.Button(self.buttons_frame, text="Left", command=lambda: self.game.execute_human_move_direction("left"))
        self.left_button.grid(row=1, column=0)
        self.right_button = tk.Button(self.buttons_frame, text="Right", command=lambda: self.game.execute_human_move_direction("right"))
        self.right_button.grid(row=1, column=2)
        self.down_button = tk.Button(self.buttons_frame, text="Down", command=lambda: self.game.execute_human_move_direction("down"))
        self.down_button.grid(row=2, column=1)

        self.disable_direction_buttons()
        self.moves_remaining = 2
        self.selected_piece = None

    def run(self):
        self.game.run()
        self.root.mainloop()

    def update_board_display(self):
        board = self.game.board
        size = board.size
        for i in range(size):
            for j in range(size):
                piece = board.grid[i][j]
                color = "white"
                text = ""
                if piece == "T":
                    text = "T"
                    color = "lightblue"
                elif piece == "O":
                    text = "O"
                    color = "lightgreen"
                self.cells[i+1][j+1].config(text=text, bg=color)

        if self.selected_piece:
            x, y = self.selected_piece
            self.cells[x+1][y+1].config(bg="orange")

    def on_cell_click(self, x, y):
        if self.game.turn != "Human":
            return

        if self.selected_piece and (x, y) == self.selected_piece:
            self.selected_piece = None
            self.disable_direction_buttons()
            self.update_board_display()
            return

        if not self.selected_piece:
            if self.game.board.grid[x][y] == "O" and self.moves_remaining > 0:
                self.selected_piece = (x, y)
                self.update_board_display()
                self.enable_direction_buttons()
            else:
                self.error("Please select one of your pieces.")
        else:
            sx, sy = self.selected_piece
            if abs(x - sx) + abs(y - sy) == 1 and self.game.board.grid[x][y] == ".":
                self.game.execute_human_move_coords(x, y)
                self.selected_piece = None
                self.moves_remaining -= 1
                self.update_board_display()
                
                if self.moves_remaining == 0:
                    self.game.end_human_turn()

    def set_info(self, text):
        self.info_label.config(text=text)

    def error(self, text):
        messagebox.showerror("Error", text)

    def game_over(self, text):
        messagebox.showinfo("Game Over", text)

    def disable_direction_buttons(self):
        self.up_button.config(state="disabled")
        self.down_button.config(state="disabled")
        self.left_button.config(state="disabled")
        self.right_button.config(state="disabled")

    def enable_direction_buttons(self):
        self.up_button.config(state="normal")
        self.down_button.config(state="normal")
        self.left_button.config(state="normal")
        self.right_button.config(state="normal")

    def enable_piece_selection(self, available_pieces):
        self.available_pieces = available_pieces
        self.highlight_available_pieces()

    def highlight_available_pieces(self):
        self.update_board_display()
        for x, y in self.available_pieces:
            if self.game.board.grid[x][y] == 'O':
                self.cells[x+1][y+1].config(bg="yellow")
