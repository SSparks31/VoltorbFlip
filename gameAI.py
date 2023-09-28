import game

class Heuristics:
    def __init__(self, i, j, val):
        self.i = i
        self.j = j
        self.val = val

class Game(game.Game):
    def heuristicsUnique(self, i, j):
        return 0
    
    def heuristicsChance(self, i, j):
        return -1
    
    def play(self): ## Sobrescreve play() do jogo original para operar utilizando IA
        print('Para avançar uma rodada, aperte enter')
        self.print()
        while True:
            heuristics = []
            for i in range(len(self._lines)):
                for j in range(len(self._columns)):
                    print(self.heuristicsBombs(i, j))
                    heuristics.append(Heuristics(i, j, self.heuristicsBombs(i, j)))

            heuristics.sort(key=lambda h: h.val)
            best = heuristics[-1]
            print(best.val)
            if best.val == -1:
                self.mark(best.i, best.j)
            elif best.val == 0:
                print('travei')
            elif best.val % 7 == 0:
                self.flip(best.i, best.j, best.val//7)
            elif best.val % 5 == 0:
                self.flip(best.i, best.j, best.val//5)
            else:
                v = int(input(('Ambiguidade - No jogo, abra o quadrado na posição ({}, {}) e informe seu valor: '.format(best.i, best.j))))
                self.flip(best.i, best.j, v)

            self.print()
            input()