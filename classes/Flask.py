
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

    def __copy__(self):
        value = self.value.copy()
        value.reverse()
        return Flask(value, self.capacity, self.order)

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

