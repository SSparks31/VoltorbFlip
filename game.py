from random import randrange

class Game:
    def __init__(self, bombs, ones, twos, threes):
        values = [0] * bombs + [1] * ones + [2] * twos + [3] * threes
        if len(values) != 25:
            raise Exception("Values must add up to 25")
        self._answer = []
        self._board = []
        self.twos = twos
        self.threes = threes
        for i in range(5):
            self._board.append([])
            self._answer.append([])
            for j in range(5):
                self._board[i].append(' ')
                v = values.pop(randrange(0, len(values)))
                self._answer[i].append(v)

    def line(self, i):
        if i not in range(len(self._answer)):
            return None
        l = self._answer[i]
        return (sum(l), sum([v == 0 for v in l]))

    def column(self, j):
        if j not in range(len(self._answer[0])):
            return None
        c = [self._answer[i][j] for i in range(len(self._answer))]
        return (sum(c), sum([v == 0 for v in c]))
        
    def flip(self, i, j):
        if self._board[i][j] != ' ':
            return
        v = self._answer[i][j]
        self.twos -= v == 2
        self.threes -= v == 3
        self._board[i][j] = v

        return v

    def won(self):
        return self.twos == 0 and self.threes == 0