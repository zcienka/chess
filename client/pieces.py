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

        # print(self.black_king.check, self.white_king.check)

        if clicked_piece == "R" or clicked_piece == "r":
            piece = "rook"
        elif clicked_piece == "B" or clicked_piece == "b":
            piece = "bishop"
        elif clicked_piece == "Q" or clicked_piece == "q":
            piece = "queen"

        if piece == "rook" or piece == "bishop" or piece == "queen":
            valid_moves = self.get_rook_queen_bishop_valid_moves(
                piece, square_x, square_y, is_white, self.board)
            valid_moves = self.get_legal_moves(
                valid_moves, clicked_piece, [square_x, square_y])
        else:
            if clicked_piece == "n" or clicked_piece == "N":
                piece = "knight"
                valid_moves = self.get_knight_valid_moves(
                    piece, square_x, square_y, is_white)
                valid_moves = self.get_legal_moves(
                    valid_moves, clicked_piece, [square_x, square_y])
            elif clicked_piece == "k" or clicked_piece == "K":
                if not is_white:
                    self.black_king.position = square
                    valid_moves = self.black_king.valid_moves
                    # valid_moves = self.get_legal_moves(self.black_king.valid_moves, clicked_piece, [square_x, square_y])

                    if valid_moves != []:
                        self.black_king.check = False

                    # print(self.black_king.check)

                    # print('self.black_king["position"]')
                    # print(self.black_king.position)
                    # print('self.black_king.valid_moves')
                    # print(self.black_king.valid_moves)
                else:
                    self.white_king.position = square
                    valid_moves = self.white_king.valid_moves
                    self.white_king.check = False
                    # valid_moves = self.get_legal_moves(self.white_king.valid_moves, clicked_piece, [square_x, square_y])

                    if valid_moves != []:
                        self.white_king.check = False

                    # print(self.white_king.check)

                    # print('self.white_king.position')
                    # print(self.white_king.position)
                    # print('self.white_king.valid_moves')
                    # print(self.white_king.valid_moves)

        self.check_collision_with_king_moves(is_white, valid_moves)

        if self.is_opponent_being_checked(valid_moves, clicked_piece):
            if is_white:
                self.black_king.check = True
            else:
                self.white_king.check = True

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
        # for move in valid_moves:
        #     if is_white:
        #         if move in self.black_king.valid_moves:
        #             self.black_king.valid_moves.remove(move)
        #     else:
        #         if move in self.white_king.valid_moves:
        #             self.white_king.valid_moves.remove(move)

        if is_white:
            for move in self.black_king.valid_moves:
                board_copy = copy.deepcopy(self.board)
                x = move[0]
                y = move[1]

                black_king = copy.deepcopy(self.black_king)
                black_king.position = [x, y]
                board_copy[x][y] = self.black_king.piece
                prev_x, prev_y = self.black_king.position
                board_copy[prev_x][prev_y] = None

                if self.is_own_king_mate(black_king.piece, board_copy, black_king):
                    self.black_king.valid_moves.remove(move)
        else:
            for move in self.white_king.valid_moves:
                board_copy = copy.deepcopy(self.board)
                x = move[0]
                y = move[1]

                white_king = copy.deepcopy(self.white_king)
                white_king.position = [x, y]

                board_copy[x][y] = self.white_king.piece
                prev_x, prev_y = self.white_king.position
                board_copy[prev_x][prev_y] = None

                if self.is_own_king_mate(white_king.piece, board_copy, white_king):
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

            if 0 <= square[0] < BOARD_SIZE and 0 <= square[1] < BOARD_SIZE:
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

    def get_white_king(self):
        return self.white_king

    def get_black_king(self):
        return self.black_king

    def set_white_king_moves(self, moves):
        self.white_king.valid_moves = moves

    def set_black_king_moves(self, moves):
        self.black_king.valid_moves = moves

    def is_own_king_mate(self, curr_piece, board, king):
        is_curr_piece_white = curr_piece.isupper()
        valid_moves = []
        piece_name = None

        for x, row in enumerate(board):
            for y, piece in enumerate(row):
                if piece != None and piece != "P" and piece != "p" and piece != "k"  and piece != "K":
                # if piece != None:
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

                    if piece == "n" or piece == "N":
                        piece_name = "knight"
                        valid_moves = self.get_knight_valid_moves(
                            piece_name, x, y, is_white)

                    # if is_curr_piece_white:
                    #     if self.white_king.position in valid_moves:
                    #         return True
                    # elif self.black_king.position in valid_moves:
                    #     return True
                    if king.position in valid_moves and king.piece.isupper() != piece.isupper():
                    # if king.position in valid_moves:
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
                    if board[x][y] == None:
                        valid_moves.append(square_copy)
                        square_copy = [piece_directions[i][0] + x,
                                       piece_directions[i][1] + y]
                    # elif board[x][y].isupper() == is_white:
                    else:
                        valid_moves.append(square_copy)
                        square_copy = [piece_directions[i][0] + x,
                                       piece_directions[i][1] + y]
                        break
                    # else:
                    #     break
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
                # elif self.board[x][y].isupper() != is_white:
                else:
                    valid_moves.append(square)

        return valid_moves

    def get_legal_moves(self, valid_moves, piece, prev_pos):
        valid_moves_copy = copy.deepcopy(valid_moves)

        for move in valid_moves_copy:
            board_copy = copy.deepcopy(self.board)
            x = move[0]
            y = move[1]
            board_copy[x][y] = piece

            prev_x = prev_pos[0]
            prev_y = prev_pos[1]

            board_copy[prev_x][prev_y] = None

            if piece.isupper():
                if self.is_own_king_mate(piece, board_copy, self.white_king):
                    valid_moves.remove(move)
            else:
                if self.is_own_king_mate(piece, board_copy, self.black_king):
                    valid_moves.remove(move)

        return valid_moves

    def is_opponent_being_checked(self, valid_moves, piece):
        for move in valid_moves:
            is_piece_white = piece.isupper()

            if not is_piece_white:
                if self.white_king.position in valid_moves:
                    return True
            elif self.black_king.position in valid_moves:
                return True

        return False

    def is_checkmate(self):
        if self.white_king.check and self.white_king.valid_moves == []:
            white = True

            if not self.are_valid_moves_left(white):
                return True
        if self.black_king.check and self.black_king.valid_moves == []:
            white = False

            if not self.are_valid_moves_left(white):
                return True

        return False

    def are_valid_moves_left(self, white):
        for x, row in enumerate(self.board):
            for y, piece in enumerate(row):
                if piece != None:
                    if piece.isupper() == white:
                        if piece == "R" or piece == "r":
                            piece = "rook"
                        elif piece == "B" or piece == "b":
                            piece = "bishop"
                        elif piece == "Q" or piece == "q":
                            piece = "queen"

                        if piece == "rook" or piece == "bishop" or piece == "queen":
                            valid_moves = self.get_rook_queen_bishop_valid_moves(
                                piece, x, y, white, self.board)
                            valid_moves = self.get_legal_moves(
                                valid_moves, piece, [x, y])
                        else:
                            if piece == "n" or piece == "N":
                                piece = "knight"
                                valid_moves = self.get_knight_valid_moves(
                                    piece, x, y, white)
                                valid_moves = self.get_legal_moves(
                                    valid_moves, piece, [x, y])
                        if len(valid_moves) != 0:
                            return True
        return False
