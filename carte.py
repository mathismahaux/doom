import pygame as pg

_ = False
mini_carte = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, 2, 2, 2, _, _, _, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, 2, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, _, _, _, 2, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, 2, 2, 2, 2, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Carte:
    def __init__(self, j):
        self.jeu = j
        self.mini_carte = mini_carte
        self.carte_monde = {}
        self.get_carte()

    def get_carte(self):
        for j, rangee in enumerate(self.mini_carte):
            for i, valeur in enumerate(rangee):
                if valeur:
                    self.carte_monde[(i, j)] = valeur

    def dessiner(self):
        [pg.draw.rect(self.jeu.ecran, 'darkgray', (pos[0]*100, pos[1]*100, 100, 100), 2)
         for pos in self.carte_monde]
