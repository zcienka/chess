import pygame
from board import Board
from game_engine import GameEngine
from constants import *
from position import Position


def main():
    running = True
    pygame.init()
    pygame.display.set_caption("Chess")
    surface = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    FPS = 60
    fen_sequence = "r1b1k1nr/p2p1p1p/n2B4/1p1NPN1P/6P1/3P1Q2/P1P1K3/q5b1/"  # mating test
    # fen_sequence = "4k3/8/4q3/8/8/8/6K1/4R3" # pin test #1
    # fen_sequence = "8/8/1Rr1k3/8/4q3/4R3/8/4K3" # pin test #2

    # fen_sequence = "r1b1k2r/pp1n1ppp/5n2/1Bb1q3/8/4N3/PPP2PPP/R1BQK2R"
    # fen_sequence = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

    board = Board(surface, WINDOW_SIZE, fen_sequence)

    pygame.display.flip()
    pygame.display.update()

    selected_piece = None
    drop_pos = False
    clock = pygame.time.Clock()

    initial_run = True

    board.draw()
    chess_board = board.get_board_from_fen_sequence()
    # game_engine.update_board(board)
    game_engine = GameEngine(chess_board)

    board.show_pieces(game_engine, initial_run)
    initial_run = False
    pygame.display.update()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                pos, piece = board.get_row_col_and_piece(
                    mouse_x, mouse_y, game_engine)

            if event.type == pygame.MOUSEBUTTONDOWN:
                board.draw()
                board.show_pieces(game_engine)

                mouse_x, mouse_y = event.pos
                pos, piece = board.get_row_col_and_piece(
                    mouse_x, mouse_y, game_engine)

                if piece != None:
                    valid_moves = game_engine.get_valid_moves(pos)
                    board.show_valid_moves(valid_moves)
                    drop_pos = True
                    selected_piece = pos, piece

                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONUP:
                if drop_pos:
                    old_pos, piece = selected_piece
                    new_pos, drop_piece = board.get_row_col_and_piece(
                        mouse_x, mouse_y, game_engine)
                    # print(new_pos.x)
                    # print(old_pos != new_pos)
                    # print([i==new_pos for i  in valid_moves])
                    print([i for i  in valid_moves])
                    

                    if old_pos != new_pos and new_pos in valid_moves:

                        if drop_piece == None or isinstance(drop_piece, str) and \
                                not (piece.isupper() == drop_piece.isupper()):

                            game_engine.update(old_pos, None)
                            game_engine.update(new_pos, piece)

                            board.convert_board_to_fen_sequence(game_engine)
                            board.draw()
                            board.show_pieces(game_engine)

                            if piece == "k" or piece == "K":
                                if piece == "k":
                                    game_engine.set_black_king_pos(new_pos)
                                else:
                                    game_engine.set_white_king_pos(new_pos)

                            board.set_king_valid_moves(game_engine)

                            if game_engine.is_checkmate():
                                print("checkmate")
                                white = piece.isupper()
                                board.show_checkmate(white, game_engine)

                selected_piece = None
                drop_pos = False
                pygame.display.update()

        clock.tick(FPS)


if __name__ == "__main__":
    main()
