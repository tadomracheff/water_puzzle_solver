import uuid
import os
import glob
from threading import Thread


class Flask:
    def __init__(self, value, capacity, order):
        self.order = order
        self.value = list()
        self.capacity = capacity
        for sip in value:
            self.value.append(sip)
        self.value.reverse()

    def __repr__(self):
        print(str(self.order) + ': ', end='')
        for sip in self.value:
            print(sip, end='|')
        print()

    def __str__(self):
        res = str(self.order) + ': '
        for sip in self.value:
            res += str(sip)
            res += '|'
        return res

    def is_assembled(self):
        if self.get_size() == self.capacity:
            if [self.value[0]] * self.get_size() == self.value:
                return True
        return False

    def get_size(self):
        return len(self.value)

    def get_top(self):
        return self.value[-1]

    def is_empty(self):
        return self.get_size() == 0

    def is_full(self):
        return self.get_size() == self.capacity

    def move_possible(self, flask):
        if self.is_empty():
            return False
        if flask.is_empty():
            return True
        if flask.is_full():
            return False
        return self.get_top() == flask.get_top()

    def move(self, flask):
        if not flask.is_full():
            if not self.is_empty():
                flask.value.append(self.value.pop())

    def __copy__(self):
        value = self.value.copy()
        value.reverse()
        return Flask(value, self.capacity, self.order)


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


def is_win(state):
    for flask in state:
        if not flask.is_empty():
            if not flask.is_assembled():
                return False

    print("WIN")
    return True


def state_equal(s1, s2):
    res = True
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            res = False
    return res


def search_loop(solution):
    for i in range(len(solution)-5):
        if i >= 2:
            if solution[i].to == solution[i - 1].where and solution[i - 1].to == solution[i].where:
                return True
        if i >= 4:
            if solution[i].to == solution[i - 3].where and solution[i - 3].to == solution[i].where:
                return True
        if i >= 3:
            if solution[i].__eq__(solution[i - 2]) and \
                    solution[i + 1].__eq__(solution[i - 1]):
                return True
        if i >= 4:
            if solution[i].__eq__(solution[i - 3]) and \
                    solution[i + 1].__eq__(solution[i - 2]) and \
                    solution[i + 2].__eq__(solution[i - 1]):
                return True
        if i >= 5:
            if solution[i].__eq__(solution[i - 4]) and \
                    solution[i + 1].__eq__(solution[i - 3]) and \
                    solution[i + 2].__eq__(solution[i - 2]) and \
                    solution[i + 3].__eq__(solution[i - 1]):
                return True
        if i >= 6:
            if solution[i].__eq__(solution[i - 5]) and \
                    solution[i + 1].__eq__(solution[i - 4]) and \
                    solution[i + 2].__eq__(solution[i - 3]) and \
                    solution[i + 3].__eq__(solution[i - 2]) and \
                    solution[i + 4].__eq__(solution[i - 1]):
                return True

    return False


def calc_current_state(node):
    # node = node_link.__copy__()
    solution = list()
    while node.parent:
        solution.append(node.move)
        node = node.parent
    state = get_copy(node.state)

    solution.reverse()

    if search_loop(solution):
        return None

    states = list()
    for move in solution:
        state = do_move(state, move)
        states.append(get_copy(state))

    return state


def do_move(state, move):
    flask_from, flask_to = None, None
    for flask in state:
        if move.where == flask.order:
            flask_from = flask
        if move.to == flask.order:
            flask_to = flask
    if flask_from and flask_to:
        flask_from.move(flask_to)

    return state


#  проверить на зацикливание
def check_limit(node):
    if node.lvl >= 100:
        # print('timeout')
        return True
    return False


def get_moves(state):
    moves = list()

    if is_win(state):
        return moves

    for flask1 in state:
        for flask2 in state:
            if flask1.order != flask2.order and flask2.move_possible(flask1):
                move = Move(flask2.order, flask1.order)
                moves.append(move)
    return moves


def get_copy(state):
    res = list()
    for flask in state:
        res.append(flask.__copy__())
    return res


def set_node(node, state):
    moves = get_moves(state)
    for move in moves:
        node.children.append(Tree(None, move, node.lvl + 1, node))


def show(state):
    for flask in state:
        flask.__repr__()


def check_solution(solution, flasks):
    state = get_copy(flasks)
    for step in solution:
        do_move(state, step)
    return is_win(state)


def show_solution(node):
    if node.children.__eq__([]):
        solution = list()
        while node.parent:
            solution.append(node.move)
            node = node.parent

        solution.reverse()
        flasks = get_copy(node.state)
        if check_solution(solution, flasks):
            unique_filename = str(uuid.uuid4())
            f = open('solution/{}_{}.txt'.format(len(solution), unique_filename), 'w')
            for step in solution:
                f.write(step.__str__() + '\n')
                print(step)


def find_solution(node):
    if node.children.__eq__([]):
        if node.win:
            show_solution(node)
    else:
        for child in node.children:
            find_solution(child)


def do(node):

    print(node.lvl)

    if node.move:
        state = calc_current_state(node)
        if not state:
            return
        if check_limit(node):
            return
        set_node(node, state)

    if node.children.__eq__([]):
        if is_win(state):
            show_solution(node)
        return
    else:
        for child in node.children:
            do(child)


def game_init(flasks_init, empty_count, capacity):
    order = 1
    flasks = list()

    for flask in flasks_init:
        flasks.append(Flask(flask, capacity, order))
        order += 1

    for i in range(empty_count):
        flasks.append(Flask((), capacity, order))
        order += 1

    return flasks


if __name__ == '__main__':
    # flasks = game_init([[1, 2], [2, 1]], 1, 2)
    # flasks = game_init([[1, 2, 3], [2, 1, 3], [2, 1, 3]], 2, 3)
    # flasks = game_init([[1, 2, 3, 1], [1, 2, 3, 3], [2, 3, 1, 2]], 2, 4)
    # flasks = game_init([[4,12,2,3],[1,9,5,7],[5,11,4,9],[3,11,1,10],[5,8,10,9],[5,12,9,3],[2,12,7,6],[1,6,7,11],[8,8,7,4],[6,10,11,2],[12,4,3,2],[1,10,6,8]], 2, 4)
    # flasks = game_init([[1,2,2,3],[4,2,5,6],[7,8,8,8],[3,7,9,4],[10,1,6,5],[3,9,11,1],[11,12,8,1],[4,12,9,10],[11,4,3,6],[5,2,5,12],[7,7,6,10],[11,12,10,9]], 2, 4)
    flasks = game_init([[1, 2, 3, 4], [2, 1, 3, 4], [2, 1, 3, 4], [4, 2, 1, 3]], 2, 4)
    # flasks = game_init([[1, 1, 1, 2], [1, 3, 2, 4], [4, 2, 4, 3], [3, 4, 3, 5], [2, 5, 5, 5]], 2, 4)

    files = glob.glob('solution/*')
    for f in files:
        os.remove(f)

    show(flasks)
    root = Tree(flasks)

    set_node(root, flasks)

    threads = list()
    for child in root.children:
        threads.append(Thread(target=do, args=(child,)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

