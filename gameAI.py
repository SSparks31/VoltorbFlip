import game

class Game(game.Game):
    def heuristics_first(self, i, j): # Regra 1: Linhas sem possibilidade de voltorb
        if (self._board[i][j] != ' '):
            return 0
        pointsLine, voltorbsLine = self.line(i)
        voltorbsFoundLine = sum(_ == 'X' for _ in self._board[i])

        pointsColumn, voltorbsColumn = self.column(j)
        voltorbsFoundColumn = sum(self._board[_][j] == 'X' for _ in range(5))
        
        return pointsLine * (voltorbsLine == voltorbsFoundLine) + pointsColumn * (voltorbsColumn == voltorbsFoundColumn)
    
    def heuristics_second(self, i, j): # Regra 2: Linhas sem possibilidade de valor
        if (self._board[i][j] != ' '):
            return 0
        pointsLine, voltorbsLine = self.line(i)
        pointsFoundLine = sum(_ for _ in self._board[i] if _ not in ('X', ' '))

        pointsColumn, voltorbsColumn = self.column(j)
        pointsFoundColumn = sum(self._board[_][j] for _ in range(5) if self._board[_][j] not in ('X', ' '))
        
        return pointsLine == pointsFoundLine or pointsColumn == pointsFoundColumn
    
    def heuristics_third(self, i, j): # Cálculo de todas as possibilidades
        if (self._board[i][j] != ' '):
            return 0
        
        pointsLine, voltorbsLine = self.line(i)
        pointsColumn, voltorbsColumn = self.column(j)
        
        voltorbsFoundLine = sum(_ == 'X' for _ in self._board[i])
        voltorbsFoundColumn = sum(self._board[_][j] == 'X' for _ in range(5))
        
        pointsFoundLine = sum(_ for _ in self._board[i] if _ not in ('X', ' '))
        pointsFoundColumn = sum(self._board[_][j] for _ in range(5) if self._board[_][j] not in ('X', ' '))
        
        possibilitiesLine: set = None
        possibilitiesColumn = None

        unflippedLine = sum(_ == ' ' for _ in self._board[i])
        unflippedColumn = sum(self._board[_][j] == ' ' for _ in range(5))

        if (unflippedLine + pointsFoundLine) == pointsLine + voltorbsLine:
            possibilitiesLine = set(('X', 1))
        
        if (unflippedColumn + pointsFoundColumn) == pointsColumn + voltorbsColumn:
            possibilitiesColumn = set(('X', 1))
        


     
    def play(self): ## Sobrescreve play() do jogo original para operar utilizando IA
        print('Para avançar uma rodada, aperte enter')
        while True:
            self.print()
            did = False
            heuristics = []
            for idx_i, _ in enumerate(self._lines):
                for idx_j, _ in enumerate(self._columns):
                    heuristics.append(((idx_i, idx_j), self.heuristics_first(idx_i, idx_j)))
            heuristics.sort(key=lambda h: h[1])
            while heuristics[-1][1] > 0:
                did = True
                (i, j), _ = heuristics.pop()
                self._board[i][j] = int(input('MOVIMENTO SEGURO - Vire o quadrado na linha {}, coluna {} e informe o valor encontrado: '.format(i+1, j+1)))

            heuristics = []
            for idx_i, _ in enumerate(self._lines):
                for idx_j, _ in enumerate(self._columns):
                    heuristics.append(((idx_i, idx_j), self.heuristics_second(idx_i, idx_j)))
            heuristics.sort(key=lambda h: h[1])
            while heuristics[-1][1] > 0:
                did = True
                (i, j), _ = heuristics.pop()
                self._board[i][j] = 'X'

            if did:
                continue
            input('Faltando a terceira heuristica')