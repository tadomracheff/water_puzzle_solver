class Tree:
    def __init__(self, state, move=None, lvl=None, parent=None):
        self.children = list()
        self.move = move
        self.state = state
        self.parent = parent
        if lvl:
            self.lvl = lvl
        else:
            self.lvl = 0
        self.win = False

    def __copy__(self):
        res = Tree(None, self.move, self.lvl, self.parent)
        return res
