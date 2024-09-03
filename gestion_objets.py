from objet_sprite import *
from pnj import *

class GestionObjets:
    def __init__(self, j):
        self.jeu = j
        self.liste_sprites = []
        self.liste_pnj = []
        self.chemin_sprites_pnj = 'ressources/sprites/pnj/'
        self.chemin_sprites_statiques = 'ressources/sprites/statiques/'
        self.chemin_sprites_animes = 'ressources/sprites/animes/'
        ajouter_sprite = self.ajouter_sprite
        ajouter_pnj = self.ajouter_pnj

        self.ajouter_sprite(ObjetSprite(j))
        self.ajouter_sprite(SpriteAnime(j))
        self.ajouter_sprite(SpriteAnime(j, p=(1.5, 1.5)))
        self.ajouter_sprite(SpriteAnime(j, p=(1.5, 7.5)))
        self.ajouter_sprite(SpriteAnime(j, p=(5.5, 3.25)))
        self.ajouter_sprite(SpriteAnime(j, p=(5.5, 4.75)))
        self.ajouter_sprite(SpriteAnime(j, p=(7.5, 2.5)))
        self.ajouter_sprite(SpriteAnime(j, p=(7.5, 5.5)))
        self.ajouter_sprite(SpriteAnime(j, p=(14.5, 1.5)))
        self.ajouter_sprite(SpriteAnime(j, c=self.chemin_sprites_animes+'flamme_rouge/0.png', p=(14.5, 7.5)))
        self.ajouter_sprite(SpriteAnime(j, c=self.chemin_sprites_animes+'flamme_rouge/0.png', p=(12.5, 7.5)))
        self.ajouter_sprite(SpriteAnime(j, c=self.chemin_sprites_animes+'flamme_rouge/0.png', p=(9.5, 7.5)))

        ajouter_pnj(Pnj(j))
    def maj(self):
        [s.maj() for s in self.liste_sprites]
        [pnj.maj() for pnj in self.liste_pnj]

    def ajouter_pnj(self, pnj):
        self.liste_pnj.append(pnj)

    def ajouter_sprite(self, sprite):
        self.liste_sprites.append(sprite)
