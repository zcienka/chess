import pygame
from constants import *
import math
from position import Position
from collections import defaultdict
import globals


class Board:
    def __init__(self, surface, fen_sequence):
        self.width = 800
        self.height = 800
        self.surface = surface
        self.white = (182, 182, 182)
        self.black = (92, 92, 92)
        self.rectangle_size = 100
        self.offset = (WINDOW_SIZE - self.width) / 2
        self.fen_sequence = fen_sequence
        self.red = (186, 69, 69)

    def draw(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.surface,
                                     self.white,
                                     pygame.Rect(self.offset + self.rectangle_size * j,
                                                 self.offset + self.rectangle_size * i,
                                                 self.rectangle_size,
                                                 self.rectangle_size))
                else:
                    pygame.draw.rect(self.surface,
                                     self.black,
                                     pygame.Rect(self.offset + self.rectangle_size * j,
                                                 self.offset + self.rectangle_size * i,
                                                 self.rectangle_size,
                                                 self.rectangle_size))

    def show_pieces(self, game, grabbed_piece_pos=None, initial_run=False):
        piece_pos = 0

        for position in self.fen_sequence:
            row = math.floor(piece_pos / BOARD_SIZE)
            col = piece_pos % BOARD_SIZE

            if position == " ":
                break

            if grabbed_piece_pos == None or Position(row, col) != grabbed_piece_pos:
                pos = Position(row, col)

                if position == "K":
                    if initial_run:
                        game.set_white_king_pos(pos)

                if position == "k":
                    if initial_run:
                        game.set_black_king_pos(pos)

                if position != "/" and not position.isdigit():
                    img = self.get_image(position)
                    self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * col,
                                                                self.offset + 0.5 * self.rectangle_size + self.rectangle_size * row)))

            if not position.isdigit():
                if position != "/":
                    piece_pos += 1
            else:
                piece_pos += int(position)

        if initial_run:
            self.set_king_valid_moves(game)

    def get_image(self, piece):
        if piece.isupper():
            return pygame.image.load(f"imgs/w_{piece}.png")
        else:
            return pygame.image.load(f"imgs/{piece}.png")

    def get_row_col_and_piece(self, mouse_x, mouse_y, game):
        col = math.floor((mouse_x - self.offset) / self.rectangle_size)
        row = math.floor((mouse_y - self.offset) / self.rectangle_size)

        if col < 0 or col >= BOARD_SIZE or row < 0 or row >= BOARD_SIZE:
            return Position(row, col), None

        board = game.get_board()

        return Position(row, col), board[row][col]

    def set_fen_sequence(self, sequence):
        self.fen_sequence = sequence

    def get_board_from_fen_sequence(self, game):
        sequence_by_rows = self.fen_sequence.split("/")
        board = []

        for i in range(len(sequence_by_rows)):
            row = []
            for piece in sequence_by_rows[i]:
                if piece == " ":
                    break
                if not piece.isdigit():
                    row.append(piece)
                else:
                    row.extend([None for _ in range(int(piece))])
            # if piece == " ":
            #     break
            board.append(row)

        parts = self.fen_sequence.split(" ")
        castling_part = parts[1]

        if "K" not in castling_part:
            game.set_short_castle_possible(False, white_king=True)
        elif "Q" not in castling_part:
            game.set_long_castle_possible(False, white_king=True)
        elif "k" not in castling_part:
            game.set_long_castle_possible(False, black_king=True)
        elif "q" not in castling_part:
            game.set_long_castle_possible(False, black_king=True)

        if len(parts) == 3:
            en_passant_move = self.chessboard_pos_to_board_coordinates(parts[2])
            game.set_pawn_double_push(en_passant_move)

        return board

    def convert_board_to_fen_sequence(self, game, en_passant_move=None):
        fen_sequence = []
        board = game.get_board()

        for row in board:
            none_count = 0

            for piece in row:
                if piece == None:
                    none_count += 1
                else:
                    if none_count != 0:
                        fen_sequence += str(none_count)
                        none_count = 0
                    fen_sequence += piece

            if none_count != 0:
                fen_sequence += str(none_count)
            fen_sequence += "/"

        white_king = game.get_white_king()
        game_board = game.get_board()

        if white_king.can_long_castle(game_board) and white_king.can_short_castle(game_board):
            fen_sequence += "KQ"
        elif white_king.can_long_castle(game_board):
            fen_sequence += "Q"
        elif white_king.can_short_castle(game_board):
            fen_sequence += "K"

        black_king = game.get_black_king()

        if black_king.can_long_castle(game_board) and black_king.can_short_castle(game_board):
            fen_sequence += "kq"
        elif black_king.can_long_castle(game_board):
            fen_sequence += "q"
        elif black_king.can_short_castle(game_board):
            fen_sequence += "k"

        if en_passant_move != None:

            fen_sequence += " " + \
                self.board_coordinates_to_chessboard_pos(en_passant_move)

        self.fen_sequence = "".join(fen_sequence)
        globals.FEN_SEQUENCE = fen_sequence

    def board_coordinates_to_chessboard_pos(self, board_coordinates):
        chessboard_col = ["a", "b", "c", "d", "e", "f", "g", "h"]
        col = chessboard_col[board_coordinates.y]
        row = BOARD_SIZE - board_coordinates.x
        return str(row) + str(col)

    def chessboard_pos_to_board_coordinates(self, chessboard_pos):
        chessboard_col = ["a", "b", "c", "d", "e", "f", "g", "h"]
        # col = chessboard_col[chessboard_pos.y]
        # row = BOARD_SIZE - chessboard_pos.x
        col = chessboard_col.index(chessboard_pos[0])
        row = BOARD_SIZE - int(chessboard_pos[1])

        return [row, col]

    def show_valid_moves(self, valid_moves, board, pos):
        curr_piece = board[pos.x][pos.y]

        for valid_move in valid_moves:
            if board[valid_move.x][valid_move.y] == None or curr_piece == None:
                circle_radius = 15
                pygame.draw.circle(self.surface,
                                   (64, 64, 64),
                                   (self.offset + self.rectangle_size * valid_move.y + self.rectangle_size / 2,
                                       self.offset + self.rectangle_size * valid_move.x + self.rectangle_size / 2),
                                   circle_radius)

            elif board[valid_move.x][valid_move.y].isupper() != curr_piece.isupper():
                circle_radius = 50
                pygame.draw.circle(self.surface,
                                   (64, 64, 64),
                                   (self.offset + self.rectangle_size * valid_move.y + self.rectangle_size / 2,
                                       self.offset + self.rectangle_size * valid_move.x + self.rectangle_size / 2),
                                   circle_radius, width=8)

    def set_king_valid_moves(self, game):
        game.reset_kings()

        game_board = game.get_board()

        for i, position in enumerate(game_board):
            for j in range(len(position)):
                if position[j] != None:
                    game.get_valid_moves(Position(i, j))

    def show_check(self, game, is_white):
        if is_white:
            king = game.get_white_king()
        else:
            king = game.get_black_king()

        x = king.position.x
        y = king.position.y

        short_castle_pos = king.get_short_castle_pos()
        long_castle_pos = king.get_long_castle_pos()

        if long_castle_pos in king.valid_moves:
            king.valid_moves.remove(long_castle_pos)
        if short_castle_pos in king.valid_moves:
            king.valid_moves.remove(short_castle_pos)

        pygame.draw.rect(self.surface,
                         self.red,
                         pygame.Rect(self.offset + self.rectangle_size * y,
                                     self.offset + self.rectangle_size * x,
                                     self.rectangle_size,
                                     self.rectangle_size))

    def get_fen_sequence(self):
        return self.fen_sequence
