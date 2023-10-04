from typing import List

class Game:
    def __init__(self, lines: List[tuple[int, int]], columns: List[tuple[int, int]]):
        self._board: List[List[str | int]] = []
        for i in range(5):
            self._board.append([])
            for j in range(5):
                self._board[i].append(' ')
        
        self._lines = lines.copy()
        self._columns = columns.copy()

    def line(self, i):
        return self._lines[i]

    def column(self, j):
        return self._columns[j]
        
    def flip(self, i, j, val):
        self._board[i][j] = val

    def print(self):
        for i in range(5):
            values = self._board[i]
            print(('  [{}]  ' * 5).format(*values) + str(self.line(i)).replace(' ', ''))
        for j in range(5):
            print(str(self.column(j)).replace(' ', '').rjust(6, ' '), end=' ')
        print('')
    
    def play(self):
        print('Modo de jogar: Insira as coordenadas de linha, coluna e valor separadas por espaço.')
        print('Para marcar ou desmarcar uma bomba, digite X no lugar do valor')
        print('Exemplo: a entrada `2 3 1` insere o valor 1 na linha 2, coluna 3')
        print('Para encerrar o jogo, aperte Ctrl + C')
        self.print()

        try:
            while True:
                py, px, val = [_ for _ in input('Entrada: ').strip().split(' ')]
                i, j = [int(_) - 1 for _ in (py, px)]
                if i not in range(len(self._lines)) or j not in range(len(self._columns)):
                    print('Posição inválida!')
                    continue
                else:
                    self.flip(i, j, val)
                self.print()
        except KeyboardInterrupt:
            pass