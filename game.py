from classes.Flask import Flask
from classes.Move import Move
from classes.Tree import Tree
from config import *
import uuid


def is_win(state):
    for flask in state:
        if not flask.is_empty():
            if not flask.is_assembled():
                return False

    print("WIN")
    return True


def search_loop(solution, capacity):
    len_solution = len(solution)

    a = solution[len_solution-1]
    k = 1
    a0 = a

    for i in range(len_solution + 1):
        if i + 1 == k:
            a0 = a
            k = k + k
        else:
            if a.__eq__(a0):
                if len_solution - k - i > capacity - 1:  # ёмкость минус 1 (нужно три хода для 1|2|2|2 -> 2|_|_|_)
                    return True
            if a.is_reverse(a0):
                return True
        if i != len_solution:
            a = solution[len_solution-1-i]

    return False


def calc_current_state(node):
    solution = list()
    while node.parent:
        solution.append(node.move)
        node = node.parent
    state = get_copy(node.state)

    solution.reverse()

    if search_loop(solution, state[0].capacity):
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


def get_moves(state):
    moves = list()

    if is_win(state):
        return moves

    for flask_from in state:
        for flask_to in state:
            if flask_to.order != flask_from.order and not flask_to.is_empty() and flask_from.move_possible(flask_to):
                move = Move(flask_from.order, flask_to.order)
                moves.append(move)

    if moves.__eq__([]):
        for flask_from in state:
            for flask_to in state:
                if flask_to.order != flask_from.order and flask_from.move_possible(
                        flask_to):
                    move = Move(flask_from.order, flask_to.order)
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
            f = open(solution_dir + '{}_{}.txt'.format(len(solution), unique_filename), 'w')
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
