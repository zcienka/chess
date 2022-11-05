import pygame
from board import Board
from rook import Rook
from constants import *

def main():
    running = True
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Chess")
    surface = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

    fen_sequence = "r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1"
    board = Board(surface, WINDOW_SIZE, fen_sequence)

    board.draw()
    board.show_pieces(WINDOW_SIZE)
    # board.show_pieces("r1b1k2r/pp1n1ppp/5n2/1Bb1q3/8/4N3/PPP2PPP/R1BQK2R", WINDOW_SIZE)
    board.convert_fen_sequence_to_board()
    # board.show_pieces("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", WINDOW_SIZE)

    pygame.display.flip()
    pygame.display.update()

    selected_piece = None
    drop_pos = False
    clock = pygame.time.Clock()

    
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
                board.show_pieces(WINDOW_SIZE)

                rook = Rook(board)
                mouse_x, mouse_y = event.pos
                row, col, piece = board.get_row_col_and_piece(mouse_x, mouse_y)

                if piece != None:
                    valid_moves = rook.get_valid_moves([row, col])
                
                    board.show_valid_moves( valid_moves)
                    drop_pos = True
                    selected_piece = row, col, piece

            if event.type == pygame.MOUSEBUTTONUP:
                if drop_pos:
                    old_row, old_col, piece = selected_piece
                    new_row, new_col, drop_piece = board.get_row_col_and_piece(mouse_x, mouse_y)

                    if old_row != new_row and old_col != new_col:
                        board.update(old_row, old_col, None)
                        board.update(new_row, new_col, piece)
                        board.convert_board_to_fen_sequence()
                        
                        board.draw()
                        board.show_pieces(WINDOW_SIZE)

                selected_piece = None
                drop_pos = False

        
        clock.tick(40)
        pygame.display.update()

    

if __name__ == "__main__":
    main()
