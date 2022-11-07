from position import Position


class King:
    def __init__(self, piece):
        self.check = False
        self.valid_moves = []
        self.position = None
        self.piece = piece
