class Move:
    def __init__(self, where, to):
        self.where = where
        self.to = to

    def __repr__(self):
        print(self.where, '->', self.to)

    def __str__(self):
        return str(self.where) + '->' + str(self.to)

    def __eq__(self, other):
        return self.to == other.to and self.where == other.where
