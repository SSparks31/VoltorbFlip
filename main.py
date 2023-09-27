from game import Game

difficulties = {
    'fácil': [6, 16, 2, 1],
    'médio': [8, 10, 4, 1],
    'difícil': [12, 2, 4, 7]
}

diff = None
while diff is None:
    diff = difficulties.get(input('Insira a dificuldade (Fácil, Médio, Difícil): ').strip().lower(), None)
game = Game(*diff)
game.play()


