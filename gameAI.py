import game

class Heuristics:
    def __init__(self, i, j, val):
        self.i = i
        self.j = j
        self.val = val

class Game(game.Game):
    def heuristicsBombs(self, i, j): # Pq não funciona aaaaaaaaaaaaaaaaaaaaaaa
        if self._board[i][j] != ' ':
            return -100 # Já marcado
        line = self._board[i]
        column = [self._board[i][j] for i in range(5)]
        pointsLine, bombsLeftLine = self.line(i)
        pointsColumn, bombsLeftColumn = self.column(j)

        valLine = sum([_ for _ in line if _ != ' '])
        valColumn = sum([_ for _ in column if _ != ' '])
        if valLine == pointsLine or valColumn == pointsColumn: # Linha/coluna alcançou seu valor máximo, portanto encontramos uma bomba
            return 100
        
        # Como ainda há números na linha/coluna, caso haja apenas um quadrado não-testado, ele é seguro
        unsolvedLine = 4 - sum([v == ' ' for v in line])
        unsolvedColumn = 4 - sum([v == ' ' for v in line])
        if unsolvedLine == 0:
            return (pointsLine - valLine) * 7 # Multiplicado para ter prioridade sobre quadrados com possibilidade de múltiplos valores
        if unsolvedColumn == 0:
            return (pointsColumn - valColumn) * 7

        possibilitiesLine = set()
        possibilitiesColumn = set()
        
        bombsFoundLine = sum([_ for _ in line if _ == 0])
        bombsFoundColumn = sum([_ for _ in column if _ == 0])
        
        if bombsFoundLine < bombsLeftLine:
            possibilitiesLine.add(0)
        if bombsFoundColumn < bombsLeftColumn:
            possibilitiesColumn.add(0)
        
        pointsLeftLine = pointsLine - valLine
        pointsLeftColumn = pointsColumn - valColumn

        for val in (1, 2, 3):
            if pointsLeftLine - val >= unsolvedLine - bombsLeftLine and pointsLeftLine <= 3 * (unsolvedLine - bombsLeftLine):
                possibilitiesLine.add(val)
            if pointsLeftColumn - val >= unsolvedColumn - bombsLeftColumn and pointsLeftColumn <= 3 * (unsolvedColumn - bombsLeftColumn):
                possibilitiesColumn.add(val)
        possibilities = possibilitiesLine.intersection(possibilitiesColumn)
        if len(possibilities) == 1:
            return possibilities.pop() * 5
        if len(possibilities) == 0:
            print('???')
        prod = 1
        for val in possibilities:
            prod *= val
        
        return prod
    
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