import copy


class Pieces:
    def __init__(self):
        self.directions = {
            "rook": [[-1, 0], [1, 0], [0, 1], [0, -1]],
            "bishop": [[-1, -1], [-1, 1], [1, 1], [1, -1]],
            "queen": [[-1, -1], [-1, 1], [1, 1], [1, -1], [-1, 0], [1, 0], [0, 1], [0, -1]],
            "knight": [[-2, 1], [-1, 2], [1, 2], [2, 1], [-1, -2], [-2, -1], [1, -2], [2, -1]],
            "king": [[-1, 0], [1, 0], [0, 1], [0, -1], [-1, -1], [-1, 1], [1, 1], [1, -1]],
            "pawn_first_move": [[1, 1], [1, 2]],
            "pawn": [[1, 1]]
        }

        self.board = []

        self.white_king = {
            "moves": [],
            "position": [],
        }

        self.black_king = {
            "moves": [],
            "position": [],
        }

    def get_valid_moves(self, square):
        valid_moves = []
        square_x = square[0]
        square_y = square[1]
        clicked_piece = self.board[square_x][square_y]
        is_white = clicked_piece.isupper()
        piece = None

        if clicked_piece == "R" or clicked_piece == "r":
            piece = "rook"
        elif clicked_piece == "B" or clicked_piece == "b":
            piece = "bishop"
        elif clicked_piece == "Q" or clicked_piece == "q":
            piece = "queen"

        if piece == "rook" or piece == "bishop" or piece == "queen":
            squares = [[square_x + direction[0], square_y + direction[1]]
                       for direction in self.directions[piece]]

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
        else:
            if clicked_piece == "n" or clicked_piece == "N":
                piece = "knight"
                squares = [[square_x + direction[0], square_y + direction[1]]
                        for direction in self.directions[piece]]
                for square in squares:
                    x = square[0]
                    y = square[1]

                    if 0 <= square[0] < 8 and 0 <= square[1] < 8:
                        if self.board[x][y] == None:
                            valid_moves.append(square)
                        elif self.board[x][y].isupper() != is_white:
                            valid_moves.append(square)
                
            elif clicked_piece == "k" or clicked_piece == "K":
                if not is_white:
                   self.black_king["position"] = square
                   valid_moves = self.black_king["moves"]
                else:
                    self.white_king["position"] = square
                    valid_moves = self.white_king["moves"]

        if clicked_piece != "k" or clicked_piece != "K":
            self.check_collision_with_king_moves(is_white, valid_moves)

        print('self.white_king["position"]')
        print(self.white_king["position"])
        print('self.white_king["moves"]')
        print(self.white_king["moves"])

        # print('self.black_king["position"]')
        # print(self.black_king["position"])
        # print('self.black_king["moves"]')
        # print(self.black_king["moves"])

        return valid_moves

    def update_board(self, board):
        self.board = board.get_board()

    def check_collision_with_king_moves(self, is_white, valid_moves):
            for move in valid_moves:
                if is_white:
                    if move in self.black_king["moves"]:
                        self.black_king["moves"].remove(move)
                else:
                    if move in self.white_king["moves"]:
                        self.white_king["moves"].remove(move)

    def set_white_king_pos(self, pos):
        self.white_king["position"] = pos
        self.white_king["moves"] = self.get_initial_king_moves(pos)
        
    def set_black_king_pos(self, pos):
        self.black_king["position"] = pos
        self.black_king["moves"] = self.get_initial_king_moves(pos)


    def get_initial_king_moves(self, pos):
        square_x = pos[0]
        square_y = pos[1]
        valid_moves = []
        clicked_piece = self.board[square_x][square_y]
        is_white = clicked_piece.isupper()


        piece = "king"
        squares = [[square_x + direction[0], square_y + direction[1]]
                for direction in self.directions[piece]]
        for square in squares:
            x = square[0]
            y = square[1]

            if 0 <= square[0] < 8 and 0 <= square[1] < 8:
                if self.board[x][y] == None:
                    valid_moves.append(square)
                elif self.board[x][y].isupper() != is_white:
                    valid_moves.append(square)
        return valid_moves

    def get_king_valid_moves(self, square):
        square_x = square[0]
        square_y = square[1]
        piece = self.board[square_x][square_y]

        is_white = piece.isupper()

        if not is_white:
            return self.black_king["moves"] 
        else:
            return self.white_king["moves"]
    
    def clear_king_moves(self):
        self.white_king["moves"] = []
        self.black_king["moves"] = []


    def get_white_king_pos(self):
        return self.white_king["position"] 

    def get_black_king_pos(self):
        return self.black_king["position"] 
    
    def set_white_king_moves(self, moves):
        self.white_king["moves"] = moves

    def set_black_king_moves(self, moves):
        self.black_king["moves"] = moves