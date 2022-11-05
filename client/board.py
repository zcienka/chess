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
        self.offset = (WINDOW_SIZE - self.width)/2
        self.fen_sequence = fen_sequence

    def draw(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.surface,
                                     self.white,
                                     pygame.Rect(self.offset + self.rectangle_size*j, self.offset + self.rectangle_size*i, self.rectangle_size, self.rectangle_size))
                else:
                    pygame.draw.rect(self.surface,
                                     self.black,
                                     pygame.Rect(self.offset + self.rectangle_size*j, self.offset + self.rectangle_size*i, self.rectangle_size, self.rectangle_size))

    def show_pieces(self, fen_sequence, WINDOW_SIZE):
        piece_pos = 0
        self.set_fen_sequence(fen_sequence)

        for i, position in enumerate(fen_sequence):
            if position == "R":
                img = self.scale_svg(WHITE_ROOK_SVG)
                self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * (piece_pos % 8),
                                                            self.offset + 0.5 * self.rectangle_size + self.rectangle_size * math.floor(piece_pos / 8))))
            elif position == "N":
                img = self.scale_svg(WHITE_KNIGHT_SVG)
                self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * (piece_pos % 8),
                                                            self.offset + 0.5 * self.rectangle_size + self.rectangle_size * math.floor(piece_pos / 8))))
            elif position == "B":
                img = self.scale_svg(WHITE_BISHOP_SVG)
                self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * (piece_pos % 8),
                                                            self.offset + 0.5 * self.rectangle_size + self.rectangle_size * math.floor(piece_pos / 8))))
            elif position == "Q":
                img = self.scale_svg(WHITE_QUEEN_SVG)
                self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * (piece_pos % 8),
                                                            self.offset + 0.5 * self.rectangle_size + self.rectangle_size * math.floor(piece_pos / 8))))
            elif position == "K":
                img = self.scale_svg(WHITE_KING_SVG)
                self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * (piece_pos % 8),
                                                            self.offset + 0.5 * self.rectangle_size + self.rectangle_size * math.floor(piece_pos / 8))))
            elif position == "P":
                img = self.scale_svg(WHITE_PAWN_SVG)
                self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * (piece_pos % 8),
                                                            self.offset + 0.5 * self.rectangle_size + self.rectangle_size * math.floor(piece_pos / 8))))

            elif position == "r":
                img = self.scale_svg(BLACK_ROOK_SVG)
                self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * (piece_pos % 8),
                                                            self.offset + 0.5 * self.rectangle_size + self.rectangle_size * math.floor(piece_pos / 8))))
            elif position == "n":
                img = self.scale_svg(BLACK_KNIGHT_SVG)
                self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * (piece_pos % 8),
                                                            self.offset + 0.5 * self.rectangle_size + self.rectangle_size * math.floor(piece_pos / 8))))
            elif position == "b":
                img = self.scale_svg(BLACK_BISHOP_SVG)
                self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * (piece_pos % 8),
                                                            self.offset + 0.5 * self.rectangle_size + self.rectangle_size * math.floor(piece_pos / 8))))
            elif position == "q":
                img = self.scale_svg(BLACK_QUEEN_SVG)
                self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * (piece_pos % 8),
                                                            self.offset + 0.5 * self.rectangle_size + self.rectangle_size * math.floor(piece_pos / 8))))
            elif position == "k":
                img = self.scale_svg(BLACK_KING_SVG)
                self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * (piece_pos % 8),
                                                            self.offset + 0.5 * self.rectangle_size + self.rectangle_size * math.floor(piece_pos / 8))))
            elif position == "p":
                img = self.scale_svg(BLACK_PAWN_SVG)
                self.surface.blit(img, img.get_rect(center=(self.offset + 0.5 * self.rectangle_size + self.rectangle_size * (piece_pos % 8),
                                                            self.offset + 0.5 * self.rectangle_size + self.rectangle_size * math.floor(piece_pos / 8))))

            if not position.isdigit():
                if position != "/":
                    piece_pos += 1
            else:
                piece_pos += int(position)

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
        a = math.floor((mouse_x - self.offset) / self.rectangle_size)
        b = math.floor((mouse_y - self.offset) / self.rectangle_size)
        sequence_by_rows = self.fen_sequence.split("/")[b]
        row = []

        for piece in sequence_by_rows:
            if not piece.isdigit():
                row.append(piece)
            else:
                row.extend([None for _ in range(int(piece))])

        return a, b, row[a]

    def set_fen_sequence(self, sequence):
        self.fen_sequence = sequence
