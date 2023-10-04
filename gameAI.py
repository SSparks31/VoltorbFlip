import game

class Game(game.Game):
    def heuristics_first(self, i, j): # Regra 1: Linhas sem possibilidade de voltorb
        if (self._board[i][j] != ' '):
            return 0
        pointsLine, voltorbsLine = self.line(i)
        voltorbsFoundLine = sum(_ == 'X' for _ in self._board[i])
        pointsFoundLine = sum(_ for _ in self._board[i] if _ not in ('X', ' '))

        pointsColumn, voltorbsColumn = self.column(j)
        voltorbsFoundColumn = sum(self._board[_][j] == 'X' for _ in range(5))
        pointsFoundColumn = sum(self._board[_][j] for _ in range(5) if self._board[_][j] not in ('X', ' '))
        
        possibilitiesLine = set(('X', 1, 2, 3))
        possibilitiesColumn = set(('X', 1, 2, 3))

        flippedLine = sum(_ != ' ' for _ in self._board[i])
        flippedColumn = sum(self._board[_][j] != ' ' for _ in range(5))

        if voltorbsLine == voltorbsFoundLine:
            possibilitiesLine = set(range(1, pointsLine  + flippedLine - pointsFoundLine - 3))
        if voltorbsColumn == voltorbsFoundColumn:
            possibilitiesColumn = set(range(1, pointsColumn + flippedColumn - pointsFoundColumn - 3))
    
        p = possibilitiesColumn.intersection(possibilitiesLine)
        return p if 'X' not in p else 0
    
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
        
        possibilitiesLine: set = set(('X', 1, 2, 3))
        possibilitiesColumn: set = set(('X', 1, 2, 3))

        unflippedLine = sum(_ == ' ' for _ in self._board[i])
        unflippedColumn = sum(self._board[_][j] == ' ' for _ in range(5))

        # Regra 3: "Soma 5"
        if unflippedLine + pointsFoundLine + voltorbsFoundLine == pointsLine + voltorbsLine:
            possibilitiesLine = set(('X', 1))
        if unflippedColumn + pointsFoundColumn + voltorbsFoundColumn == pointsColumn + voltorbsColumn:
            possibilitiesColumn = set(('X', 1))

        # Regra 4: Há apenas um valor na linha
        if voltorbsLine == 4:
            possibilitiesLine = set(('X', pointsLine))
        if voltorbsColumn == 4:
            possibilitiesColumn = set(('X', pointsColumn))

        # Regra 5: "Soma 6"
        if unflippedLine + pointsFoundLine + voltorbsFoundLine == pointsLine + voltorbsLine + 1:
            possibilitiesLine = set(('X', 1, 2))
        if unflippedColumn + pointsFoundColumn + voltorbsFoundColumn == pointsColumn + voltorbsColumn + 1:
            possibilitiesColumn = set(('X', 1, 2))
        
        # Regra 6: Sem possibilidade de 1
        if unflippedLine + pointsFoundLine + voltorbsFoundLine == pointsLine + voltorbsLine + 1:
            possibilitiesLine = set(('X', 1, 2))
        if unflippedColumn + pointsFoundColumn + voltorbsFoundColumn == pointsColumn + voltorbsColumn + 1:
            possibilitiesColumn = set(('X', 1, 2))

        # Regra 7: Interseção linhas e colunas
        return possibilitiesColumn.intersection(possibilitiesLine)

     
    def play(self): ## Sobrescreve play() do jogo original para operar utilizando IA
        print('Para avançar uma rodada, aperte enter')
        print('Para encerrar, aperte Ctrl+C')
        while any([_ == ' ' for line in self._board for _ in line]):
            self.print()
            did = False

            heuristics = []
            for idx_i, _ in enumerate(self._lines):
                for idx_j, _ in enumerate(self._columns):
                    v = self.heuristics_first(idx_i, idx_j)
                    if v != 0:
                        heuristics.append(((idx_i, idx_j), v))
            heuristics.sort(key=lambda h: len(h[1]), reverse=True)
            if heuristics:
                did = True
                (i, j), p = heuristics.pop()
                if len(p) == 1:
                    self._board[i][j] = p.pop()
                else:
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

            heuristics = []
            for idx_i, _ in enumerate(self._lines):
                for idx_j, _ in enumerate(self._columns):
                    h = self.heuristics_third(idx_i, idx_j)
                    if h != 0:
                        heuristics.append(((idx_i, idx_j), h))
            if all([set(('X' , 1)) == _[1] for _ in heuristics]):
                print('Só restam Voltorbs e 1s')
                return
            safeMovements = [_ for _ in heuristics if 'X' not in _[1]]
            if safeMovements:
                heuristics = safeMovements # Não interagir com espaços perigosos
                heuristics.sort(key=lambda h: len(h[1]), reverse=True)
            else:
                heuristics.sort(key=lambda h: len(h[1]) * (2 in h[1] or 3 in h[1])) # Prioridade a espaços que podem ser 2 ou 3

            if heuristics:
                did = True
                (i, j), p = heuristics.pop()
                if len(p) == 1:
                    self._board[i][j] = p.pop()
                elif 'X' not in p: 
                    self._board[i][j] = int(input('MOVIMENTO SEGURO - Vire o quadrado na linha {}, coluna {} e informe o valor encontrado: '.format(i+1, j+1)))
                else:
                    v = input('MOVIMENTO PERIGOSO - Vire o quadrado na linha {}, coluna {} e informe o valor encontrado: '.format(i+1, j+1))
                    try:
                        self._board[i][j] = int(v)
                    except:
                        self._board[i][j] = v
            if did:
                continue
            
        print('Jogo encerrado')
        self.print()