import pygame
from constants import *
import io
import cairosvg
import math
from position import Position
from collections import defaultdict


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

        self.piece_imgs = defaultdict(list, {
            "R": self.scale_svg(WHITE_ROOK_SVG),
            "N": self.scale_svg(WHITE_KNIGHT_SVG),
            "B": self.scale_svg(WHITE_BISHOP_SVG),
            "Q": self.scale_svg(WHITE_QUEEN_SVG),
            "K": self.scale_svg(WHITE_KING_SVG),
            "P": self.scale_svg(WHITE_PAWN_SVG),
            "r": self.scale_svg(BLACK_ROOK_SVG),
            "n": self.scale_svg(BLACK_KNIGHT_SVG),
            "b": self.scale_svg(BLACK_BISHOP_SVG),
            "q": self.scale_svg(BLACK_QUEEN_SVG),
            "k": self.scale_svg(BLACK_KING_SVG),
            "p": self.scale_svg(BLACK_PAWN_SVG)
        })

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

    def show_pieces(self, game_engine, grabbed_piece_pos=None, initial_run=False):
        piece_pos = 0

        for i, position in enumerate(self.fen_sequence):
            row = math.floor(piece_pos / BOARD_SIZE)
            col = piece_pos % BOARD_SIZE

            if grabbed_piece_pos == None or Position(row, col) != grabbed_piece_pos:
                pos = Position(row, col)

                if position == "K":
                    if initial_run:
                        game_engine.set_white_king_pos(pos)

                if position == "k":
                    if initial_run:
                        game_engine.set_black_king_pos(pos)

                if position != "/" and not position.isdigit():
                    img = self.piece_imgs[position]
                    self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * col,
                                                                self.offset + 0.5 * self.rectangle_size + self.rectangle_size * row)))

                

            if not position.isdigit():
                if position != "/":
                    piece_pos += 1
            else:
                piece_pos += int(position)

        if initial_run:
            self.set_king_valid_moves(game_engine)

    def scale_svg(self, svg_file):
        DPI = 100
        _scale = 2
        _svg = " ".join(svg_file.split())

        _svg = cairosvg.svg2svg(_svg, dpi=(DPI / _scale))
        _bytes = cairosvg.svg2png(_svg)
        byte_io = io.BytesIO(_bytes)
        img = pygame.image.load(byte_io)

        return img

    def get_row_col_and_piece(self, mouse_x, mouse_y, game_engine):
        col = math.floor((mouse_x - self.offset) / self.rectangle_size)
        row = math.floor((mouse_y - self.offset) / self.rectangle_size)

        if col < 0 or col >= BOARD_SIZE or row < 0 or row >= BOARD_SIZE:
            return Position(row, col), None

        board = game_engine.get_board()

        return Position(row, col), board[row][col]

    def set_fen_sequence(self, sequence):
        self.fen_sequence = sequence

    def get_board_from_fen_sequence(self):
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
        # self.board = board
        return board

    def convert_board_to_fen_sequence(self, game_engine):
        fen_sequence = []
        board = game_engine.get_board()

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

        self.fen_sequence = "".join(fen_sequence)

    def show_valid_moves(self, valid_moves):
        circle_radius = 15

        for valid_move in valid_moves:
            pygame.draw.circle(self.surface,
                               (64, 64, 64),
                               (self.offset + self.rectangle_size * valid_move.y + self.rectangle_size / 2,
                                self.offset + self.rectangle_size * valid_move.x + self.rectangle_size / 2),
                               circle_radius)

    def set_king_valid_moves(self, game_engine):
        game_engine.clear_king_moves()
        white_king = game_engine.get_white_king()
        black_king = game_engine.get_black_king()

        w_moves = game_engine.get_initial_king_moves(white_king.position)
        b_moves = game_engine.get_initial_king_moves(black_king.position)

        game_engine.set_white_king_moves(w_moves)
        game_engine.set_black_king_moves(b_moves)

        game_board = game_engine.get_board()

        for i, position in enumerate(game_board):
            for j in range(len(position)):
                if position[j] != None:
                    game_engine.get_valid_moves(Position(i, j))

    def show_checkmate(self, is_white, game_engine):
        if is_white:
            black_king = game_engine.get_black_king()
            x = black_king.position.x
            y = black_king.position.y

            pygame.draw.rect(self.surface,
                             self.red,
                             pygame.Rect(self.offset + self.rectangle_size * y, self.offset + self.rectangle_size * x,
                                         self.rectangle_size,
                                         self.rectangle_size))
        else:
            white_king = game_engine.get_white_king()
            x = white_king.position.x
            y = white_king.position.y

            pygame.draw.rect(self.surface,
                             self.red,
                             pygame.Rect(self.offset + self.rectangle_size * y, self.offset + self.rectangle_size * x,
                                         self.rectangle_size,
                                         self.rectangle_size))

    def get_piece_img(self, piece):
        return self.piece_imgs[piece]
