from game import Game

def print_game(game):
    for i in range(5):
        values = game._board[i]
        print(('  [{}]  ' * 5).format(*values) + str(game.line(i)).replace(' ', ''))
    for j in range(5):
        print(str(game.column(j)).replace(' ', '').rjust(6, ' '), end=' ')
    print('')

difficulties = {
    'fácil': [6, 16, 2, 1],
    'médio': [8, 10, 4, 1],
    'difícil': [12, 2, 4, 7]
}

diff = None
while diff is None:
    diff = difficulties.get(input('Insira a dificuldade (Fácil, Médio, Difícil): ').strip().lower(), None)
game = Game(*diff)

print_game(game)
while True:
    try:
        py, px = [int(_) - 1 for _ in input('Insira a posição: ').strip().split(' ')]
    except:
        print('Formato inválido!')
        continue
    if px not in range(5) or py not in range(5):
        print('Posição inválida!')
        continue
    
    v = game.flip(py, px)
    print_game(game)
    
    if v == 0:
        print('Morreu!')
        break

    if game.won():
        print('Ganhou!')
        break


