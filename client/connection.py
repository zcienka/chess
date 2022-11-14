from constants import *
import socket
import sys
import globals

class Connection:
      def __init__(self, host, port, board):
         self.host = host
         self.port = port
         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.board = board

      # def refresh(self, surface, board, game):
         # surface.fill((0, 0, 0))
         # game.set_board(board)

      def receive(self):
         while True:
            try:
               request = self.client.recv(128)
               decoded_request = request.decode()

               if not self.is_command(decoded_request) and decoded_request != "1" and decoded_request != "0" and decoded_request != "":
                  print("decoded_request: ", decoded_request)
                  globals.FEN_SEQUENCE = decoded_request
                  self.board.set_fen_sequence(globals.FEN_SEQUENCE)
               # else:
               #    self.check_command(decoded_request)


            except socket.error as e:
               print(e)
               sys.exit(0)

      def send(self, data):
         try:
            self.client.send(str.encode(data))
         except socket.error as e:
            print(e)
            sys.exit(0)

      def connect(self):
         try:
            self.client.connect((self.host, self.port))
            self.client.send(str.encode(ASSIGN_COLOR))
            color = self.client.recv(128)
            globals.ASSIGNED_COLOR = color.decode()
            print("color: ", color.decode())
         except socket.error as e:
            print(e)
            sys.exit(0)

      def is_command(self, request):
         return request in [DISCONNECT_OPPONENT, SERVER_DISCONNECTED]

      def check_command(self, command):
         if command == DISCONNECT_OPPONENT:
            pass
         elif command == SERVER_DISCONNECTED:
            sys.exit(0)
         elif command == ASSIGN_COLOR:
            pass
            # ASSIGNED_COLOR
