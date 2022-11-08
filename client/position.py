class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if other == None:
            return False
        return self.x == other.x and self.y == other.y

    # def __contains__(self, other):
    #     print(other.x)    