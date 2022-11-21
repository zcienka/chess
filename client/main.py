import pygame
from board import Board
from game import Game
from constants import *
import globals
import copy
import threading
from connection import Connection
from popup_window import PopupWindow
from position import Position
import os

surface = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

board = Board(surface, globals.FEN_SEQUENCE)

board.draw()
game = Game()
chess_board = board.get_board_from_fen_sequence(game, initial_run=True)
game.set_board(chess_board)
pygame.init()

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
    elif game.is_black_in_check():
        globals.BLACK_CHECK = True

    if game.is_checkmate():
        globals.IS_CHECKMATE = True

    if game.is_stalemate():
        globals.IS_STALEMATE = True


def display_popups(is_click, mouse_x, mouse_y):
    if globals.SERVER_ERROR:
        if is_click:
            popupWindow.display_server_disconnected(Position(mouse_x, mouse_y))
        else:
            popupWindow.display_server_disconnected()
    elif globals.OPPONENT_DISCONNECTED:
        if is_click:
            popupWindow.display_opponent_disconnected(Position(mouse_x, mouse_y))
        else:
            popupWindow.display_opponent_disconnected()
    elif globals.IS_CHECKMATE:
        if is_click:
            popupWindow.display_checkmate(Position(mouse_x, mouse_y))
        else:
            popupWindow.display_checkmate()
    elif globals.IS_DRAW:
        if is_click:
            popupWindow.display_draw(Position(mouse_x, mouse_y))
        else:
            popupWindow.display_draw()
    elif globals.OPPONENT_NOT_CONNECTED_YET:
        popupWindow.display_waiting_for_opponent()



def main():
    pygame.display.set_caption("Chess")
    MAX_FPS = 60

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
    valid_moves = []
    is_click = False

    mouse_x = None
    mouse_y  = None

    connection.connect()

    if not globals.SERVER_ERROR:
        receive_thread = threading.Thread(target=connection.receive)
        receive_thread.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    connection.disconnect()
                    os._exit(0)

            elif event.type == pygame.QUIT:
                pygame.quit()
                connection.disconnect()
                os._exit(0)

            if event.type == pygame.MOUSEMOTION:
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
                is_click = True

                if piece != None:
                    if globals.IS_WHITES_TURN == piece.isupper() \
                        and piece.isupper() == globals.ASSIGNED_COLOR \
                            and not globals.SERVER_ERROR:
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

                    if old_pos != new_pos and new_pos in valid_moves:
                        if drop_piece == None or isinstance(drop_piece, str) and \
                                not (piece.isupper() == drop_piece.isupper()):
                            valid_moves = []
                            globals.WHITE_CHECK = False
                            globals.BLACK_CHECK = False
                            update_game(piece, old_pos, new_pos)

        surface.fill(BLACK)
        board.draw()

        if globals.WHITE_CHECK:
            board.show_check(game, is_white=True)
        elif globals.BLACK_CHECK:
            board.show_check(game, is_white=False)

        board.show_pieces(game, drag_pos)

        if valid_moves != [] and not globals.SERVER_ERROR:
            board.show_valid_moves(valid_moves, game.get_board(), clicked_pos)

        if drag and piece_img != None:
            x = mouse[0] - piece_img.get_height() / 2
            y = mouse[1] - piece_img.get_width() / 2
            surface.blit(piece_img, tuple([x, y]))

        display_popups(is_click, mouse_x, mouse_y)
        is_click = False

        pygame.display.update()

        clock.tick(MAX_FPS)


if __name__ == "__main__":
    main()
