import pygame
from board import Board

WINDOW_SIZE = 900

def main():
    running = True
    pygame.init()
    pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Chess")
    surface = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    fen_sequence = "r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1"
    board = Board(surface, WINDOW_SIZE, fen_sequence)

    board.draw()
    board.show_pieces(fen_sequence, WINDOW_SIZE)
    # board.show_pieces("r1b1k2r/pp1n1ppp/5n2/1Bb1q3/8/4N3/PPP2PPP/R1BQK2R", WINDOW_SIZE)
    
    # board.show_pieces("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", WINDOW_SIZE)

    pygame.display.flip()
    pygame.display.update()

    selected_piece = None
    
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
                if piece != None:
                    selected_piece = piece, row, col
            if event.type == pygame.MOUSEBUTTONUP:
                selected_piece = None

    

if __name__ == "__main__":
    main()
