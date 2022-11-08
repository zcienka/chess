from position import Position
from constants import BOARD_SIZE
import globals


class Pawns:
    def __init__(self, is_white):
        self.initial_pawn_positions = []
        self.double_push = None
        self.is_white = is_white
        self.first_move = [[-1, 0], [-2, 0]]
        self.move = [[-1, 0]]
        self.capture_moves = [[-1, 1], [-1, -1]]

        if is_white:
            self.initial_pawn_positions = [Position(6, i) for i in range(8)]
            self.promotion_list = [Position(0, i) for i in range(8)]
        else:
            self.initial_pawn_positions = [Position(1, i) for i in range(8)]
            self.promotion_list = [Position(7, i) for i in range(8)]

    def is_first_move(self, pos):
        return pos in self.initial_pawn_positions

    def is_en_passant_possible(self, pos, opponent_double_push):
        # if globals.IS_WHITES_TURN:
        if opponent_double_push == None:
            return False
        return (pos.y == opponent_double_push.y + 1 or pos.y == opponent_double_push.y - 1) and pos.x == opponent_double_push.x

        # return (pos.y == opponent_double_push.y + 1 or pos.y == opponent_double_push.y - 1) and pos.x == opponent_double_push.x

        # return (pos.x == opponent_double_push.x + 1 or pos.x == opponent_double_push.x - 1) and and

    def set_double_push(self, pos):
        self.double_push = pos

    def clear_double_push(self):
        self.double_push = None

    def get_double_push(self):
        return self.double_push

    def get_en_passant_move(self, opponent_double_push):
        if globals.IS_WHITES_TURN:
            return Position(opponent_double_push.x - 1, opponent_double_push.y)

        return Position(opponent_double_push.x + 1, opponent_double_push.y)

    def get_possible_capturing_moves(self, pos, board):
        if globals.IS_WHITES_TURN:
            possible_captures = [Position(pos.x + move[0], pos.y + move[1])
                                 for move in self.capture_moves]
        else:
            possible_captures = [Position(pos.x - move[0], pos.y - move[1])
                                 for move in self.capture_moves]

        valid_captures = []

        for capture in possible_captures:
            if 0 <= capture.x < BOARD_SIZE and 0 <= capture.y < BOARD_SIZE:
                point = board[capture.x][capture.y]

                if point != None:
                    if point.isupper() != globals.IS_WHITES_TURN:
                        valid_captures.append(capture)

        return valid_captures

    def get_moves(self, pos, board, opponent_double_push):
        # self.clear_double_push()
        capturing_moves = self.get_possible_capturing_moves(pos, board)

        if pos in self.initial_pawn_positions:
            if globals.IS_WHITES_TURN:
                valid_moves = [Position(pos.x + move[0], pos.y + move[1])
                               for move in self.first_move]
            else:
                valid_moves = [Position(pos.x - move[0], pos.y - move[1])
                               for move in self.first_move]

            for move in valid_moves:
                if board[move.x][move.y] != None:
                    valid_moves.remove(move)

            valid_moves.extend(capturing_moves)
        else:
            if globals.IS_WHITES_TURN:
                valid_moves = [Position(pos.x + move[0], pos.y + move[1])
                               for move in self.move]
            else:
                valid_moves = [Position(pos.x - move[0], pos.y - move[1])
                               for move in self.move]

            for move in valid_moves:
                if board[move.x][move.y] != None:
                    valid_moves.remove(move)

            valid_moves.extend(capturing_moves)

            if opponent_double_push != None:
                if self.is_en_passant_possible(pos, opponent_double_push):
                    en_passant_move = self.get_en_passant_move(
                        opponent_double_push)
                    print("EN PASSANT")
                    valid_moves.append(en_passant_move)

        return valid_moves

    def is_double_move(self, prev_move, curr_move):
        if globals.IS_WHITES_TURN:
            if prev_move.x - 2 == curr_move.x and curr_move.y == prev_move.y:
                return True
        elif prev_move.x + 2 == curr_move.x and curr_move.y == prev_move.y:
            return True

        return False

    def set_double_move(self, pos):
        self.double_push = pos

    def is_promotion(self, pos):
        return pos in self.promotion_list


    def is_en_passant_move(self, pos, opponent_double_push):
        if opponent_double_push == None:
            return False

        if globals.IS_WHITES_TURN:
            return pos.x + 1 == opponent_double_push.x and pos.y == opponent_double_push.y
        else:
            return pos.x - 1 == opponent_double_push.x and pos.y == opponent_double_push.y




