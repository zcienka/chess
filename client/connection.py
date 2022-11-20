from constants import *
import socket
import os
import globals


class Connection:
    def __init__(self, host, port, board, game, popupWindow):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.board = board
        self.game = game
      #   self.is_opponent_connected = False
      #   self.popupWindow = popupWindow

    def receive(self):
        while True:
            try:
               # if globals.OPPONENT_NOT_CONNECTED_YET:
               #    self.send(IS_OPPONENT_CONNECTED)
               #    print("kurwa")

               request = self.client.recv(128)
               decoded_request = request.decode()
               print("decoded_request: ", decoded_request)

               if self.is_command(decoded_request):
                  pass
               #    self.check_command(decoded_request)

               else:
                  #  if decoded_request == OPPONENT_CONNECTED:
                  #   globals.IS_OPPONENT_CONNECTED = True
                  globals.OPPONENT_NOT_CONNECTED_YET = False

                  # if not self.is_command(decoded_request):
                  globals.FEN_SEQUENCE = decoded_request
                  self.board.set_fen_sequence(globals.FEN_SEQUENCE)
                  board = self.board.get_board_from_fen_sequence(
                        self.game)
                  self.game.set_board(board)
                  self.board.set_king_valid_moves(self.game)

                  globals.WHITE_CHECK = False
                  globals.BLACK_CHECK = False

                  if self.game.is_white_in_check():
                        globals.WHITE_CHECK = True
                  if self.game.is_black_in_check():
                        globals.BLACK_CHECK = True

                  globals.IS_WHITES_TURN = not globals.IS_WHITES_TURN

                              # if globals.OPPONENT_NOT_CONNECTED_YET:

            except socket.error as e:
                  os._exit(1)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error as e:
            os._exit(1)

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            self.client.send(str.encode(ASSIGN_COLOR))
            color = self.client.recv(128)
            globals.ASSIGNED_COLOR = int(color.decode())
            # print("color: ", color.decode())

            # self.send(IS_OPPONENT_CONNECTED)
            # self.client.send(str.encode(IS_OPPONENT_CONNECTED))

            # self.client.send(str.encode(IS_OPPONENT_CONNECTED))
            # self.send(IS_OPPONENT_CONNECTED)

            # globals.OPPONENT_NOT_CONNECTED_YET = not bool(int(self.client.recv(128).decode()))
               # if globals.OPPONENT_NOT_CONNECTED_YET:
            # if not is_opponent_connected:
            #  PopupWindow.display_user_connecting()
            # else:
            # if is_opponent_connected:
            #  self.is_opponent_connected = True
            # globals.IS_OPPONENT_CONNECTED = self.client.recv(128)
            # if
        except socket.error as e:
            os._exit(1)

    def is_command(self, request):
        return request in [OPPONENT_DISCONNECTED, SERVER_DISCONNECTED, WAITING_FOR_USER, OPPONENT_CONNECTED, OPPONENT_CONNECTING]

    def check_command(self, command):
        print("check_command")
        if command == OPPONENT_DISCONNECTED:
            print("opponent disconnected")
        elif command == SERVER_DISCONNECTED:
            os._exit(1)
        elif command == WAITING_FOR_USER:
            print("waiting for the user")
        elif command == OPPONENT_CONNECTED:
            print("xd")
            globals.OPPONENT_NOT_CONNECTED_YET = False
        elif command == OPPONENT_CONNECTING:
            globals.OPPONENT_NOT_CONNECTED_YET = True
            # self.send(IS_OPPONENT_CONNECTED)

