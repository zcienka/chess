import pygame
from board import Board
from game import Game
from constants import *
import globals
import copy
import threading
from connection import Connection
import sys
from popup_window import PopupWindow

surface = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

globals.FEN_SEQUENCE = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR KQkq"
board = Board(surface, globals.FEN_SEQUENCE)

board.draw()
game = Game()
chess_board = board.get_board_from_fen_sequence(game, initial_run=True)
game.set_board(chess_board)

popupWindow = PopupWindow(surface)

host = "192.168.134.128"
port = 5050
connection = Connection(host, port, board, game, popupWindow)


def update_game(piece, old_pos, new_pos):
    if game.is_king(piece):
        game.check_and_perform_castling(new_pos)

    game.update(old_pos, None)
    game.update(new_pos, piece)

    is_double_pawn_move = False

    if game.is_pawn(piece):
        if game.is_pawn_double_move(old_pos, new_pos):
            game.set_pawn_double_push(new_pos)
            is_double_pawn_move = True

        opponent_pawn_pos = game.get_opponent_pawn_position()

        if game.is_promotion(new_pos):
            if globals.IS_WHITES_TURN:
                game.update(new_pos, "Q")
            else:
                game.update(new_pos, "q")

        if game.is_en_passant_move(new_pos, opponent_pawn_pos):
            game.update(opponent_pawn_pos, None)

    if is_double_pawn_move:
        board.convert_board_to_fen_sequence(game, new_pos)
    else:
        board.convert_board_to_fen_sequence(game)

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

    fen_sequence = board.get_fen_sequence()
    connection.send(fen_sequence)

    if game.is_white_in_check():
        globals.WHITE_CHECK = True
        print("white check")
    if game.is_black_in_check():
        globals.BLACK_CHECK = True
        print("black check")


    if game.is_checkmate():
        print("checkmate")

    if game.is_stalemate():
        print("stalemate")




def main():
    pygame.init()
    pygame.display.set_caption("Chess")
    FPS = 60

    pygame.display.flip()
    pygame.display.update()

    selected_piece = None
    drop_pos = False
    clock = pygame.time.Clock()

    initial_run = True
    drag_pos = None

    board.show_pieces(game, None, initial_run)
    initial_run = False
    pygame.display.update()

    piece_img = None
    pos = None
    drag = False
    checkmate = False
    valid_moves = []

    connection.connect()

    receive_thread = threading.Thread(target=connection.receive)
    receive_thread.start()

    while True:
        for event in pygame.event.get():
            # if not drag:
                #   board.set_fen_sequence(globals.FEN_SEQUENCE)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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

                print(pos.x, pos.y)

                clicked_pos = copy.deepcopy(pos)

                if piece != None:
                    if globals.IS_WHITES_TURN == piece.isupper() and piece.isupper() == globals.ASSIGNED_COLOR:
                        if drag == False:
                            drag_pos = pos
                            piece_img = board.get_image(piece)

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

                    print("new_pos", new_pos.x, new_pos.y)
                    

                    if old_pos != new_pos and new_pos in valid_moves:
                        if drop_piece == None or isinstance(drop_piece, str) and \
                                not (piece.isupper() == drop_piece.isupper()):
                            valid_moves = []
                            globals.WHITE_CHECK = False
                            globals.BLACK_CHECK = False
                            update_game(piece, old_pos, new_pos)

        surface.fill((0, 0, 0))
        board.draw()


        if globals.WHITE_CHECK:
                board.show_check(game, is_white=True)
        elif globals.BLACK_CHECK:
                board.show_check(game, is_white=False)

        board.show_pieces(game, drag_pos)

        if valid_moves != []:
            board.show_valid_moves(valid_moves, game.get_board(), clicked_pos)

        if drag and piece_img != None:
            x = mouse[0] - piece_img.get_height() / 2
            y = mouse[1] - piece_img.get_width() / 2
            surface.blit(piece_img, tuple([x, y]))

        # if globals.OPPONENT_NOT_CONNECTED_YET:
            # popupWindow.display()
                            # if not globals.OPPONENT_NOT_CONNECTED_YET:
            # print("IS_OPPONENT_CONNECTED")
        


        pygame.display.update() 

        clock.tick(FPS)


if __name__ == "__main__":
    main()
