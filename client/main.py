import pygame
from board import Board
from pieces import Pieces
from constants import *


def main():
    running = True
    pygame.init()
    pygame.display.set_caption("Chess")
    surface = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

    fen_sequence = "r1b1k1nr/p2p1p1p/n2B4/1p1NPN1P/6P1/3P1Q2/P1P1K3/q5b1/"
    # fen_sequence = "r1b1k2r/pp1n1ppp/5n2/1Bb1q3/8/4N3/PPP2PPP/R1BQK2R"
    # fen_sequence = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

    board = Board(surface, WINDOW_SIZE, fen_sequence)

    pygame.display.flip()
    pygame.display.update()

    selected_piece = None
    drop_pos = False
    clock = pygame.time.Clock()

    pieces = Pieces()
    initial_run = True

    board.draw()
    board.convert_fen_sequence_to_board()
    pieces.update_board(board)
    board.show_pieces(pieces, initial_run)
    initial_run = False

    while running:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                row, col, piece = board.get_row_col_and_piece(mouse_x, mouse_y)

            if event.type == pygame.MOUSEBUTTONDOWN:
                board.draw()
                board.show_pieces(pieces)
                pieces.update_board(board)

                mouse_x, mouse_y = event.pos
                row, col, piece = board.get_row_col_and_piece(mouse_x, mouse_y)

                if piece != None:
                    valid_moves = pieces.get_valid_moves([row, col])
                    # print(valid_moves)
                    board.show_valid_moves(valid_moves)
                    drop_pos = True
                    selected_piece = row, col, piece

            if event.type == pygame.MOUSEBUTTONUP:
                if drop_pos:
                    old_row, old_col, piece = selected_piece
                    new_row, new_col, drop_piece = board.get_row_col_and_piece(
                        mouse_x, mouse_y)

                    print([new_row, new_col] in valid_moves)
                    if [old_row, old_col] != [new_row, new_col] and [new_row, new_col] in valid_moves:
                        board.update(old_row, old_col, None)
                        board.update(new_row, new_col, piece)

                        board.convert_board_to_fen_sequence()

                        board.draw()
                        board.show_pieces(pieces)

                        if piece == "k" or piece == "K":
                            if piece == "k":
                                pieces.set_black_king_pos([new_row, new_col])
                            else:
                                pieces.set_white_king_pos([new_row, new_col])

                        board.set_king_valid_moves(pieces)

    

                selected_piece = None
                drop_pos = False

        clock.tick(40)
        pygame.display.update()


if __name__ == "__main__":
    main()
