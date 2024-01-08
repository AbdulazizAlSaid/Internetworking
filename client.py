import tkinter as tk
from tkinter import messagebox
import socket
import threading
from tictactoe import TicTacToe

def start_client():
    host = 'localhost'
    port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    game_mode = input("Choose game mode ('human' or 'computer'): ").lower()

    return client_socket, game_mode

def update_client_move(client_socket, row, col):
    client_socket.send(f"{row},{col}".encode())

def receive_data(client_socket, game):
    def update_board_and_show_message():
        game.update_board()
        messagebox.showinfo("Game Over", "Player X wins!")

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break

        print(f"Received data from Player 1: {data}")
        if data == "GAME_OVER":
            game.reset_game()
            client_window.after(1000, update_board_and_show_message)
        else:
            row, col = map(int, data.split(','))
            game.make_move(row, col)

if __name__ == '__main__':
    client_socket, game_mode = start_client()
    client_window = tk.Tk()
    client_window.title("Tic Tac Toe")
    game = TicTacToe(client_window, client_socket, game_mode)

    threading.Thread(target=receive_data, args=(client_socket, game)).start()

    client_window.mainloop()