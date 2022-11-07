class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x

    # def __contains__(self, other):
    #     print(other.x)