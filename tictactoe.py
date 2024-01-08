import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root, connection, game_mode):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.connection = connection
        self.game_mode = game_mode
        if self.game_mode == "computer":
            self.computer_player = 'O' if self.current_player == 'X' else 'X'

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                button = tk.Button(root, text='', width=10, height=4, command=lambda i=i, j=j: self.make_move(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def make_move(self, row, col):
        if self.game_mode == "computer" and self.current_player == self.computer_player:
            self.make_computer_move()

        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            winner = self.check_winner()
            if winner:
                messagebox.showinfo("Game Over", f"Player {winner} wins!")
                self.reset_game()
            elif all(self.board[i][j] != ' ' for i in range(3) for j in range(3)):
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.connection.send(f"{row},{col}".encode())
                self.update_board()

                # If it's now the computer's turn, make its move immediately
                if self.game_mode == "computer" and self.current_player == self.computer_player:
                    self.make_computer_move()

    def make_computer_move(self):
        import random
        available_moves = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']
        if available_moves:
            row, col = random.choice(available_moves)
            self.board[row][col] = self.computer_player
            self.buttons[row][col].config(text=self.computer_player)
            winner = self.check_winner()
            if winner:
                messagebox.showinfo("Game Over", f"Player {winner} wins!")
                self.reset_game()
            elif all(self.board[i][j] != ' ' for i in range(3) for j in range(3)):
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.connection.send(f"{row},{col}".encode())
                self.update_board()

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        return None

    def reset_game(self):
        try:
            self.current_player = 'X'
            self.board = [[' ' for _ in range(3)] for _ in range(3)]

            for i in range(3):
                for j in range(3):
                    self.buttons[i][j].config(text='')
        except Exception as e:
            print(f"Error in reset_game: {e}")

    def update_board(self):
        try:
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j].config(text=self.board[i][j])
        except Exception as e:
            print(f"Error in update_board: {e}")
