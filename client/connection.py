from constants import *
import socket
import globals


class Connection:
    def __init__(self, host, port, board, game, popupWindow):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.board = board
        self.game = game
        self.popupWindow = popupWindow

    def receive(self):
        while True:
            try:
                response = self.client.recv(128)
                decoded_response = response.decode().strip()
                print("decoded_response: ", decoded_response)

                if self.is_command(decoded_response):
                    self.check_command(decoded_response)

                else:
                    globals.OPPONENT_NOT_CONNECTED_YET = False

                    globals.FEN_SEQUENCE = decoded_response
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
            except:
                globals.SERVER_ERROR = True


    def send(self, data):
        try:
            # data = data + "\n"
            print("data ", data)
            self.client.send(str.encode(data))
        except:
            globals.SERVER_ERROR = True

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            self.send(ASSIGN_COLOR)
            color = self.client.recv(128)
            globals.ASSIGNED_COLOR = int(color.decode())

            self.send(IS_OPPONENT_CONNECTED)
            response = self.client.recv(128).decode()

            if response == OPPONENT_CONNECTED:
                globals.OPPONENT_NOT_CONNECTED_YET = False
        except:
            globals.SERVER_ERROR = True

    def is_command(self, response):
        return response in [OPPONENT_DISCONNECTED, OPPONENT_CONNECTED]

    def check_command(self, command):
        if command == OPPONENT_DISCONNECTED:
            globals.OPPONENT_DISCONNECTED = True
            print("opponent disconnected")
        elif command == OPPONENT_CONNECTED:
            globals.OPPONENT_NOT_CONNECTED_YET = False

    def disconnect(self):
        self.send(DISCONNECT_USER)

