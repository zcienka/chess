import pygame
from constants import *
import svgutils
import io
import cairosvg
import math


class Board:
    def __init__(self, surface, WINDOW_SIZE, fen_sequence):
        self.width = 800
        self.height = 800
        self.surface = surface
        self.white = (182, 182, 182)
        self.black = (92, 92, 94)
        self.rectangle_size = 100
        self.offset = (WINDOW_SIZE - self.width) / 2
        self.fen_sequence = fen_sequence
        self.board = []

    def draw(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.surface,
                                     self.white,
                                     pygame.Rect(self.offset + self.rectangle_size * j, self.offset + self.rectangle_size*i, self.rectangle_size, self.rectangle_size))
                else:
                    pygame.draw.rect(self.surface,
                                     self.black,
                                     pygame.Rect(self.offset + self.rectangle_size * j, self.offset + self.rectangle_size*i, self.rectangle_size, self.rectangle_size))

    def show_pieces(self, pieces, initial_run=False):
        piece_pos = 0

        for i, position in enumerate(self.fen_sequence):
            row = math.floor(piece_pos / BOARD_SIZE)
            col = piece_pos % BOARD_SIZE

            if position == "R":
                img = self.scale_svg(WHITE_ROOK_SVG)
            elif position == "N":
                img = self.scale_svg(WHITE_KNIGHT_SVG)
            elif position == "B":
                img = self.scale_svg(WHITE_BISHOP_SVG)
            elif position == "Q":
                img = self.scale_svg(WHITE_QUEEN_SVG)
            elif position == "K":
                img = self.scale_svg(WHITE_KING_SVG)

                if initial_run:
                    pieces.set_white_king_pos([row, col])
            elif position == "P":
                img = self.scale_svg(WHITE_PAWN_SVG)
            elif position == "r":
                img = self.scale_svg(BLACK_ROOK_SVG)
            elif position == "n":
                img = self.scale_svg(BLACK_KNIGHT_SVG)
            elif position == "b":
                img = self.scale_svg(BLACK_BISHOP_SVG)
            elif position == "q":
                img = self.scale_svg(BLACK_QUEEN_SVG)
            elif position == "k":
                img = self.scale_svg(BLACK_KING_SVG)

                if initial_run:
                    pieces.set_black_king_pos([row, col])
            elif position == "p":
                img = self.scale_svg(BLACK_PAWN_SVG)

            if position != "/" and not position.isdigit():
                self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * col,
                                                            self.offset + 0.5 * self.rectangle_size + self.rectangle_size * row)))

            if not position.isdigit():
                if position != "/":
                    piece_pos += 1
            else:
                piece_pos += int(position)

        if initial_run:
            self.set_king_valid_moves(pieces)

    def scale_svg(self, svg_file):
        DPI = 100
        _scale = 2
        _svg = " ".join(svg_file.split())

        _svg = cairosvg.svg2svg(_svg, dpi=(DPI / _scale))
        _bytes = cairosvg.svg2png(_svg)
        byte_io = io.BytesIO(_bytes)
        img = pygame.image.load(byte_io)

        return img

    def get_row_col_and_piece(self, mouse_x, mouse_y):
        col = math.floor((mouse_x - self.offset) / self.rectangle_size)
        row = math.floor((mouse_y - self.offset) / self.rectangle_size)

        if col < 0 or col >= BOARD_SIZE or row < 0 or row >= BOARD_SIZE:
            return col, row, None

        return row, col, self.board[row][col]

    def set_fen_sequence(self, sequence):
        self.fen_sequence = sequence

    def convert_fen_sequence_to_board(self):
        sequence_by_rows = self.fen_sequence.split("/")
        board = []

        for i in range(BOARD_SIZE):
            row = []
            for piece in sequence_by_rows[i]:
                if not piece.isdigit():
                    row.append(piece)
                else:
                    row.extend([None for _ in range(int(piece))])
            board.append(row)
        self.board = board

    def update(self, row, col, piece):
        self.board[row][col] = piece

    def convert_board_to_fen_sequence(self):
        fen_sequence = []

        for row in self.board:
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

        self.fen_sequence = "".join(fen_sequence)

    def get_board(self):
        return self.board

    def show_valid_moves(self, valid_moves):
        circle_radius = 15

        for valid_move in valid_moves:
            pygame.draw.circle(self.surface,
                               (64, 64, 64),
                               (self.offset + self.rectangle_size * valid_move[1] + self.rectangle_size / 2,
                                self.offset + self.rectangle_size * valid_move[0] + self.rectangle_size / 2),
                               circle_radius)

    def set_king_valid_moves(self, pieces):
        pieces.clear_king_moves()
        white_king = pieces.get_white_king()
        black_king = pieces.get_black_king()

        w_moves = pieces.get_initial_king_moves(white_king.position)
        b_moves = pieces.get_initial_king_moves(black_king.position)

        pieces.set_white_king_moves(w_moves)
        pieces.set_black_king_moves(b_moves)

        for i, position in enumerate(self.board):
            for j in range(len(position)):
                if position[j] != None:
                    pieces.get_valid_moves([i, j])

    def show_checkmate(self, is_white, pieces):
        circle_radius = 15

        if is_white:
            black_king = pieces.get_black_king()
            x = black_king.position[0]
            y = black_king.position[1]

            pygame.draw.rect(self.surface,
                             (255, 0, 0),
                             pygame.Rect(self.offset + self.rectangle_size * y, self.offset + self.rectangle_size * x,
                                         self.rectangle_size,
                                         self.rectangle_size), 2)
        else:
            white_king = pieces.get_white_king()
            x = white_king.position[0]
            y = white_king.position[1]

            pygame.draw.rect(self.surface,
                             (255, 0, 0),
                             pygame.Rect(self.offset + self.rectangle_size * y, self.offset + self.rectangle_size * x,
                                         self.rectangle_size,
                                         self.rectangle_size), 2)
