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

    def get_board_from_fen_sequence(self):
        sequence_by_rows = self.fen_sequence.split("/")
        board = []

        for i in range(len(sequence_by_rows)):
            row = []
            for piece in sequence_by_rows[i]:
                # if piece == " ":
                #     break
                if not piece.isdigit():
                    row.append(piece)
                else:
                    row.extend([None for _ in range(int(piece))])
            # if piece == " ":
            #     break
            board.append(row)

        # last_part = sequence_by_rows[-1].split(" ")

        # if last_part[0] == "w":
            # globals.IS_WHITES_TURN = True
        # elif last_part[0] == "b":
            # globals.IS_WHITES_TURN = False
        

        # if last_part[1] == "Kqkq":
        #     game.set
            

        
        return board

    def convert_board_to_fen_sequence(self, game):
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
        
        # if globals.IS_WHITES_TURN:
        #     fen_sequence += " w "
        # else:
        #     fen_sequence += " b "

        # white_king = game.get_white_king()

        # if white_king.can_long_castle() and white_king.can_short_castle():
        #     fen_sequence += "KQ"
        # elif white_king.can_long_castle():
        #     fen_sequence += "Q"
        # elif white_king.can_short_castle():
        #     fen_sequence += "K"
        
        # black_king = game.get_black_king()

        # if black_king.can_long_castle() and black_king.can_short_castle():
        #     fen_sequence += "kq"
        # elif black_king.can_long_castle():
        #     fen_sequence += "q"
        # elif black_king.can_short_castle():
        #     fen_sequence += "k"

        self.fen_sequence = "".join(fen_sequence)

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
