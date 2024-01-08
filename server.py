import socket
import threading
import tkinter as tk
from tkinter import messagebox
from tictactoe import TicTacToe

def start_server():
    host = 'localhost'
    port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Waiting for Player 2 to connect on {host}:{port}")
    connection, address = server_socket.accept()
    print(f"Player 2 connected from {address}")

    game_mode = input("Choose game mode ('human' or 'computer'): ").lower()

    return connection, game_mode

def receive_data(connection, game):
    def update_board_and_show_message():
        game.update_board()
        messagebox.showinfo("Game Over", "Player O wins!")

    while True:
        data = connection.recv(1024).decode()
        if not data:
            break

        print(f"Received data from Player 2: {data}")
        if data == "WIN" or data == "TIE":
            game.reset_game()
            server_window.after(1000, update_board_and_show_message)
            connection.send("GAME_OVER".encode())
        else:
            row, col = map(int, data.split(','))
            game.make_move(row, col)

if __name__ == '__main__':
    connection, game_mode = start_server()
    server_window = tk.Tk()
    server_window.title("Tic Tac Toe - Server")
    game = TicTacToe(server_window, connection, game_mode)

    threading.Thread(target=receive_data, args=(connection, game)).start()

    server_window.mainloop()