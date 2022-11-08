import pygame
from board import Board
from game_engine import GameEngine
from constants import *
from copy import deepcopy
import globals


def main():
    running = True
    pygame.init()
    pygame.display.set_caption("Chess")
    surface = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    FPS = 60

    # fen_sequence = "r1b1k1nr/p2p1p1p/n2B4/1p1NPN1P/6P1/3P1Q2/P1P1K3/q5b1/"  # mating test
    # fen_sequence = ""
    # fen_sequence = "4k3/8/4q3/8/8/8/6K1/4R3" # pin test #1
    # fen_sequence = "8/8/1Rr1k3/8/4q3/4R3/8/4K3" # pin test #2

    # fen_sequence = "r1b1k2r/pp1n1ppp/5n2/1Bb1q3/8/4N3/PPP2PPP/R1BQK2R"
    fen_sequence = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

    board = Board(surface, fen_sequence)

    pygame.display.flip()
    pygame.display.update()

    selected_piece = None
    drop_pos = False
    clock = pygame.time.Clock()

    initial_run = True

    board.draw()
    chess_board = board.get_board_from_fen_sequence()
    game_engine = GameEngine(chess_board)

    board.show_pieces(game_engine, None, initial_run)
    initial_run = False
    pygame.display.update()

    piece_img = None
    pos = None
    drag = False
    drag_pos = None
    checkmate = False
    valid_moves = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse = event.pos
                mouse_x, mouse_y = mouse
                pos, piece = board.get_row_col_and_piece(
                    mouse_x, mouse_y, game_engine)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = event.pos
                valid_moves = []

                mouse_x, mouse_y = mouse
                pos, piece = board.get_row_col_and_piece(
                    mouse_x, mouse_y, game_engine)
                print(pos.x, pos.y)

                if globals.IS_WHITES_TURN == piece.isupper():
                    if drag == False:
                        drag_pos = pos
                        piece_img = board.get_piece_img(piece)

                    if piece != None:
                        valid_moves = game_engine.get_valid_moves(pos)
                        board.show_valid_moves(valid_moves)
                        drop_pos = True
                        selected_piece = pos, piece
                        drag = True

            elif event.type == pygame.MOUSEBUTTONUP:
                piece_img = None
                drag_pos = None
                drag = False

                if drop_pos:
                    old_pos, piece = selected_piece
                    new_pos, drop_piece = board.get_row_col_and_piece(
                        mouse_x, mouse_y, game_engine)

                    if old_pos != new_pos and new_pos in valid_moves:
                        if drop_piece == None or isinstance(drop_piece, str) and \
                                not (piece.isupper() == drop_piece.isupper()):
                            valid_moves = []
                            game_engine.update(old_pos, None)
                            game_engine.update(new_pos, piece)

                            if piece == "p" or piece == "P":
                                if game_engine.is_pawn_double_move(old_pos, new_pos):
                                    print("pawn double move")
                                    game_engine.set_pawn_double_push(new_pos)
                                else:
                                    print("not double move")
                                
                                opponent_pawn_pos = game_engine.get_opponent_pawn_position()

                                if game_engine.is_en_passant_move(new_pos, opponent_pawn_pos):
                                    game_engine.update(opponent_pawn_pos, None)

                                if game_engine.is_promotion(new_pos):
                                    if globals.IS_WHITES_TURN:
                                        game_engine.update(new_pos, "Q")
                                    else:
                                        game_engine.update(new_pos, "q")

                            board.convert_board_to_fen_sequence(game_engine)

                            if piece == "k" or piece == "K":
                                if piece == "k":
                                    game_engine.set_black_king_pos(new_pos)
                                else:
                                    game_engine.set_white_king_pos(new_pos)

                            board.set_king_valid_moves(game_engine)

                            game_engine.clear_opponent_double_push()

                            globals.IS_WHITES_TURN = not globals.IS_WHITES_TURN

                            if game_engine.is_checkmate():
                                print("checkmate")
                                white = piece.isupper()
                                checkmate = True

        board.draw()

        if checkmate:
            board.show_checkmate(white, game_engine)

        board.show_pieces(game_engine, drag_pos)

        if valid_moves != []:
            board.show_valid_moves(valid_moves)

        if drag and piece_img != None:
            x = mouse[0] - piece_img.get_height() / 2
            y = mouse[1] - piece_img.get_width() / 2
            surface.blit(piece_img, tuple([x, y]))

        pygame.display.update()

        clock.tick(FPS)


if __name__ == "__main__":
    main()
