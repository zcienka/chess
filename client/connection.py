from constants import *
import socket
import os
import globals
from popup_window import PopupWindow

class Connection:
      def __init__(self, host, port, board, game):
         self.host = host
         self.port = port
         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.board = board
         self.game = game

      def receive(self):
         while True:
            try:
               request = self.client.recv(128)
               decoded_request = request.decode()

               if not self.is_command(decoded_request) and decoded_request != "1" and decoded_request != "0" and decoded_request != "":
                  print("decoded_request: ", decoded_request)
                  globals.FEN_SEQUENCE = decoded_request
                  self.board.set_fen_sequence(globals.FEN_SEQUENCE)
                  board = self.board.get_board_from_fen_sequence(self.game)
                  self.game.set_board(board)
                  self.board.set_king_valid_moves(self.game)

                  globals.WHITE_CHECK = False
                  globals.BLACK_CHECK = False

                  if self.game.is_white_in_check():
                        globals.WHITE_CHECK = True
                        print("white check")
                  if self.game.is_black_in_check():
                        globals.BLACK_CHECK = True
                        print("black check")

                  globals.IS_WHITES_TURN = not globals.IS_WHITES_TURN
               # else:
               #    self.check_command(decoded_request)


            except socket.error as e:
               
               print(e)
               # os._exit(1)
               

      def send(self, data):
         try:
            self.client.send(str.encode(data))
         except socket.error as e:
            print(e)
            os._exit(1)


      def connect(self):
         try:
            self.client.connect((self.host, self.port))
            self.client.send(str.encode(ASSIGN_COLOR))
            color = self.client.recv(128)
            globals.ASSIGNED_COLOR = int(color.decode())
            print("color: ", color.decode())
         except socket.error as e:
            PopupWindow.display_server_not_connected()
            # print(e)
            # os._exit(1)

      def is_command(self, request):
         return request in [DISCONNECT_OPPONENT, SERVER_DISCONNECTED]

      def check_command(self, command):
         if command == DISCONNECT_OPPONENT:
            pass
         elif command == SERVER_DISCONNECTED:
            os._exit(1)
         elif command == WAITING_FOR_USER:
            pass

