class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, o):
        if o == None:
            return False
        return self.x == o.x and self.y == o.y
