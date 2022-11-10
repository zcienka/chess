import pygame
from board import Board
from game import GameEngine
from constants import *
import globals
from position import Position
import copy
import threading
import socket
import sys


host = "192.168.134.128"
port = 5050
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
opp_move = []
cc = []

def send(data):
    try:
        client.send(str.encode(data))
        return client.recv(128).decode()
    except socket.error as e:
        print(e)

def connect():
    try:
        client.connect((host, port))
        client.send(str.encode("Get color"))
        return client.recv(128).decode()
    except:
        pass

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

    # fen_sequence = "k7/7R/8/8/8/8/8/2Q4K" # stalemate test

    board = Board(surface, fen_sequence)

    pygame.display.flip()
    pygame.display.update()

    selected_piece = None
    drop_pos = False
    clock = pygame.time.Clock()

    initial_run = True

    board.draw()
    chess_board = board.get_board_from_fen_sequence()
    game = GameEngine(chess_board)

    board.show_pieces(game, None, initial_run)
    initial_run = False
    pygame.display.update()

    piece_img = None
    pos = None
    drag = False
    drag_pos = None
    checkmate = False
    valid_moves = []
    white_check = False
    black_check = False


    # client.connect((host, port))
    lol = connect()
    print(lol)

    # receive_thread = threading.Thread(target=receive)
    # receive_thread.start()
    
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
                    mouse_x, mouse_y, game)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = event.pos
                valid_moves = []

                mouse_x, mouse_y = mouse
                pos, piece = board.get_row_col_and_piece(
                    mouse_x, mouse_y, game)
                
                clicked_pos = copy.deepcopy(pos)

                if piece != None:
                    if globals.IS_WHITES_TURN == piece.isupper():
                        if drag == False:
                            drag_pos = pos
                            piece_img = board.get_piece_img(piece)



                        valid_moves = game.get_valid_moves(pos)
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
                        mouse_x, mouse_y, game)

                    if old_pos != new_pos and new_pos in valid_moves:
                        if drop_piece == None or isinstance(drop_piece, str) and \
                                not (piece.isupper() == drop_piece.isupper()):
                            valid_moves = []
                            white_check = False
                            black_check = False

                            if game.is_king(piece):
                                game.check_and_perform_castling(pos)

                            game.update(old_pos, None)
                            game.update(new_pos, piece)

                            if game.is_pawn(piece):
                                if game.is_pawn_double_move(old_pos, new_pos):
                                    print("pawn double move")
                                    game.set_pawn_double_push(new_pos)
                                else:
                                    print("not double move")

                                opponent_pawn_pos = game.get_opponent_pawn_position()

                                if game.is_en_passant_move(new_pos, opponent_pawn_pos):
                                    game.update(opponent_pawn_pos, None)

                                if game.is_promotion(new_pos):
                                    if globals.IS_WHITES_TURN:
                                        game.update(new_pos, "Q")
                                    else:
                                        game.update(new_pos, "q")

                            board.convert_board_to_fen_sequence(game)

                            xd = board.get_fen_sequence()
                            receive = send(xd)
                            print("receive")
                            print(receive)
                            # message = client.recv(1024)

                            if game.is_rook(piece):
                                game.set_rook_has_moved(old_pos)

                            if piece == "k":
                                game.set_black_king_pos(new_pos)
                                game.set_black_king_has_moved()
                            elif piece == "K":
                                game.set_white_king_pos(new_pos)
                                game.set_white_king_has_moved()

                            board.set_king_valid_moves(game)

                            game.clear_opponent_double_push()

                            globals.IS_WHITES_TURN = not globals.IS_WHITES_TURN

                            if game.is_checkmate():
                                print("checkmate")

                            if game.is_stalemate():
                                print("stalemate")

                            if game.is_white_in_check():
                                white_check = True
                            if game.is_black_in_check():
                                black_check = True  

        surface.fill((0, 0, 0))
        board.draw()

        if white_check:
            board.show_check(game, is_white=True)
        if black_check:
            board.show_check(game, is_white=False)

        board.show_pieces(game, drag_pos)

        if valid_moves != []:
            board.show_valid_moves(valid_moves, game.get_board(), clicked_pos)

        if drag and piece_img != None:
            x = mouse[0] - piece_img.get_height() / 2
            y = mouse[1] - piece_img.get_width() / 2
            surface.blit(piece_img, tuple([x, y]))

        pygame.display.update()

        clock.tick(FPS)


if __name__ == "__main__":
    main()
