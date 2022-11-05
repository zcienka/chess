import copy


class Rook:
    def __init__(self, board):
        # self.directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        self.directions = {
            "rook": [[-1, 0], [1, 0], [0, 1], [0, -1]],
            "bishop": [[-1, -1], [-1, 1], [1, 1], [1, -1]],
            "queen": [[-1, -1], [-1, 1], [1, 1], [1, -1], [-1, 0], [1, 0], [0, 1], [0, -1]]
        }

        self.board = board.get_board()

    def get_valid_moves(self, square):
        valid_moves = []

        square_x = square[0]
        square_y = square[1]
        clicked_piece = self.board[square_x][square_y]
        
        if clicked_piece == "R" or clicked_piece == "r":
            piece = "rook"
        elif clicked_piece == "B" or clicked_piece == "b":
            piece = "bishop"
        elif clicked_piece == "Q" or clicked_piece == "q":
            piece = "queen"

        squares = [[square_x + direction[0], square_y + direction[1]]
              for direction in self.directions[piece]]

        is_white = False


        is_white = clicked_piece.isupper()

        for i, square in enumerate(squares):
            curr_square = copy.deepcopy(square)

            while True:
                x = curr_square[0]
                y = curr_square[1]
                piece_directions = self.directions[piece]

                if 0 <= x < 8 and 0 <= y < 8:
                    if self.board[x][y] == None:
                        valid_moves.append(curr_square)
                        curr_square = [
                            piece_directions[i][0] + curr_square[0], piece_directions[i][1] + curr_square[1]]
                    elif self.board[x][y].isupper() != is_white:
                        valid_moves.append(curr_square)
                        curr_square = [
                            piece_directions[i][0] + curr_square[0], piece_directions[i][1] + curr_square[1]]
                        break
                    else:
                        break
                else:
                    break

        return valid_moves
