import copy
from king import King
from constants import *


class Pieces:
    def __init__(self):
        self.directions = {
            "rook": [[-1, 0], [1, 0], [0, 1], [0, -1]],
            "bishop": [[-1, -1], [-1, 1], [1, 1], [1, -1]],
            "queen": [[-1, -1], [-1, 1], [1, 1], [1, -1], [-1, 0], [1, 0], [0, 1], [0, -1]],
            "knight": [[-2, 1], [-1, 2], [1, 2], [2, 1], [-1, -2], [-2, -1], [1, -2], [2, -1]],
            "king": [[-1, 0], [1, 0], [0, 1], [0, -1], [-1, -1], [-1, 1], [1, 1], [1, -1]],
            "pawn_first_move": [[1, 1], [1, 2]],
            "pawn": [[1, 1]]
        }

        self.board = []

        self.white_king = King("K")
        self.black_king = King("k")

    def get_valid_moves(self, square):
        square_x = square[0]
        square_y = square[1]
        clicked_piece = self.board[square_x][square_y]
        is_white = self.board[square_x][square_y].isupper()
        valid_moves = []

        piece = None

        if clicked_piece == "R" or clicked_piece == "r":
            piece = "rook"
        elif clicked_piece == "B" or clicked_piece == "b":
            piece = "bishop"
        elif clicked_piece == "Q" or clicked_piece == "q":
            piece = "queen"

        if piece == "rook" or piece == "bishop" or piece == "queen":
            valid_moves = self.get_rook_queen_bishop_valid_moves(
                piece, square_x, square_y, is_white, self.board)
            valid_moves = self.get_legal_moves(valid_moves, clicked_piece, [square_x, square_y])
        else:
            if clicked_piece == "n" or clicked_piece == "N":
                piece = "knight"
                valid_moves = self.get_knight_valid_moves(
                    piece, square_x, square_y, is_white)
            elif clicked_piece == "k" or clicked_piece == "K":
                if not is_white:
                    self.black_king.position = square
                    valid_moves = self.black_king.valid_moves

                    # print('self.black_king["position"]')
                    # print(self.black_king.position)
                    # print('self.black_king.valid_moves')
                    # print(self.black_king.valid_moves)
                else:
                    self.white_king.position = square
                    valid_moves = self.white_king.valid_moves

                    # print('self.white_king.position')
                    # print(self.white_king.position)
                    # print('self.white_king.valid_moves')
                    # print(self.white_king.valid_moves)

        self.check_collision_with_king_moves(is_white, valid_moves)

        # print('self.white_king["position"]')
        # print(self.white_king.position)
        # print('self.white_kingvalid_moves')
        # print(self.white_king.valid_moves)

        # print('self.black_king["position"]')
        # print(self.black_king["position"])
        # print('self.black_king["moves"]')
        # print(self.black_king["moves"])

        return valid_moves

    def update_board(self, board):
        self.board = board.get_board()

    def check_collision_with_king_moves(self, is_white, valid_moves):
        for move in valid_moves:
            if is_white:
                if move in self.black_king.valid_moves:
                    self.black_king.valid_moves.remove(move)
            else:
                if move in self.white_king.valid_moves:
                    self.white_king.valid_moves.remove(move)

    def set_white_king_pos(self, pos):
        self.white_king.position = pos
        self.white_king.moves = self.get_initial_king_moves(pos)

    def set_black_king_pos(self, pos):
        self.black_king.position = pos
        self.black_king.moves = self.get_initial_king_moves(pos)

    def get_initial_king_moves(self, pos):
        square_x = pos[0]
        square_y = pos[1]
        valid_moves = []
        clicked_piece = self.board[square_x][square_y]
        is_white = clicked_piece.isupper()

        piece = "king"
        squares = [[square_x + direction[0], square_y + direction[1]]
                   for direction in self.directions[piece]]
        for square in squares:
            x = square[0]
            y = square[1]

            if 0 <= square[0] < 8 and 0 <= square[1] < 8:
                if self.board[x][y] == None:
                    valid_moves.append(square)
                elif self.board[x][y].isupper() != is_white:
                    valid_moves.append(square)
        return valid_moves

    def get_king_valid_moves(self, square):
        square_x = square[0]
        square_y = square[1]
        piece = self.board[square_x][square_y]

        is_white = piece.isupper()

        if not is_white:
            return self.black_king.valid_moves
        else:
            return self.white_king.valid_moves

    def clear_king_moves(self):
        self.white_king.valid_moves = []
        self.black_king.valid_moves = []

    def get_white_king_pos(self):
        return self.white_king.position

    def get_black_king_pos(self):
        return self.black_king.position

    def set_white_king_moves(self, moves):
        self.white_king.valid_moves = moves

    def set_black_king_moves(self, moves):
        self.black_king.valid_moves = moves

    def is_own_king_mate(self, curr_piece, board):
        # curr_move_x = curr_move[0]
        # curr_move_y = curr_move[1]
        # curr_piece = self.board[x][y]
        is_curr_piece_white = curr_piece.isupper()
        valid_moves = []
        piece_name = None

        for x, row in enumerate(board):
            for y, piece in enumerate(row):
                if piece != None:
                    is_white = piece.isupper()
                    if piece == "R" or piece == "r":
                        piece_name = "rook"
                    elif piece == "B" or piece == "b":
                        piece_name = "bishop"
                    elif piece == "Q" or piece == "q":
                        piece_name = "queen"

                    if piece_name == "rook" or piece_name == "bishop" or piece_name == "queen":
                        valid_moves = self.get_rook_queen_bishop_valid_moves(
                            piece_name, x, y, is_white, board)

                    if is_curr_piece_white:
                        if self.white_king.position in valid_moves:
                            return True
                        # self.black_king.mate = True
                    elif self.black_king.position in valid_moves:
                        # self.white_king.mate = True
                        return True
        return False

    def get_rook_queen_bishop_valid_moves(self, piece, square_x, square_y, is_white, board):
        valid_moves = []
        squares = [[square_x + direction[0], square_y + direction[1]]
                   for direction in self.directions[piece]]

        for i, square in enumerate(squares):
            square_copy = copy.deepcopy(square)

            while True:
                x = square_copy[0]
                y = square_copy[1]
                piece_directions = self.directions[piece]

                if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                    # board_copy[x][y] = None
                    # board_copy[square_x][square_y] = piece

                    # if self.is_own_king_mate(piece, board_copy):
                        # break
                    if board[x][y] == None:
                        valid_moves.append(square_copy)
                        square_copy = [piece_directions[i][0] + x,
                                       piece_directions[i][1] + y]
                    elif board[x][y].isupper() != is_white:
                        valid_moves.append(square_copy)
                        square_copy = [piece_directions[i][0] + x,
                                       piece_directions[i][1] + y]
                        break
                    else:
                        break
                else:
                    break
        return valid_moves

    def get_knight_valid_moves(self, piece, x, y, is_white):
        valid_moves = []
        squares = [[x + direction[0], y + direction[1]]
                   for direction in self.directions[piece]]
        for square in squares:
            x = square[0]
            y = square[1]

            if 0 <= square[0] < BOARD_SIZE and 0 <= square[1] < BOARD_SIZE:
                if self.board[x][y] == None:
                    valid_moves.append(square)
                elif self.board[x][y].isupper() != is_white:
                    valid_moves.append(square)

        return valid_moves

    def get_legal_moves(self, valid_moves, piece, prev_pos):
        valid_moves_copy =  copy.deepcopy(valid_moves)
        
        for move in valid_moves_copy: 
            board_copy = copy.deepcopy(self.board)
            x = move[0]
            y = move[1]
            board_copy[x][y] = piece

            prev_x = prev_pos[0]
            prev_y = prev_pos[1]

            board_copy[prev_x][prev_y] = None

            if self.is_own_king_mate(piece, board_copy):
                valid_moves.remove(move)


        return valid_moves


