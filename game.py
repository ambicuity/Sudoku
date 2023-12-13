import tkinter as tk
from tkinter import messagebox
import random

class SudokuGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Game")

        self.grid_size = 9
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.solution = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.generate_puzzle()

        self.create_widgets()

    def generate_puzzle(self):
        # Generate a random Sudoku puzzle
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.solution = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.solve_sudoku()

        # Remove some numbers to create a puzzle
        for _ in range(40):  # Adjust the number of hidden cells as needed
            row, col = random.randint(0, 8), random.randint(0, 8)
            self.board[row][col] = 0

    def solve_sudoku(self):
        # Backtracking algorithm to solve the Sudoku puzzle
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid_move(i, j, num):
                            self.board[i][j] = num
                            if self.solve_sudoku():
                                return True
                            self.board[i][j] = 0
                    return False
        return True

    def is_valid_move(self, row, col, num):
        # Check if placing 'num' at (row, col) is a valid move
        for i in range(self.grid_size):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[box_start_row + i][box_start_col + j] == num:
                    return False

        return True

    def create_widgets(self):
        self.entry_grid = [[None] * self.grid_size for _ in range(self.grid_size)]

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                entry = tk.Entry(self.master, width=3, font=('Arial', 14), justify='center')
                entry.grid(row=i, column=j)
                entry.insert(0, str(self.board[i][j]) if self.board[i][j] != 0 else "")
                entry.config(state='disabled' if self.board[i][j] != 0 else 'normal')
                self.entry_grid[i][j] = entry

        solve_button = tk.Button(self.master, text="Solve", command=self.solve_button_click)
        solve_button.grid(row=self.grid_size, columnspan=self.grid_size)

    def solve_button_click(self):
        # Solve the puzzle and display the solution
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.entry_grid[i][j].get()
                if not value:
                    self.board[i][j] = 0
                else:
                    try:
                        self.board[i][j] = int(value)
                    except ValueError:
                        messagebox.showerror("Error", "Invalid input. Please enter integers.")
                        return

        if self.solve_sudoku():
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    self.entry_grid[i][j].delete(0, tk.END)
                    self.entry_grid[i][j].insert(0, str(self.board[i][j]))
                    self.entry_grid[i][j].config(state='disabled')
        else:
            messagebox.showinfo("No Solution", "The puzzle has no solution. Please check your input.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGame(root)
    root.mainloop()
