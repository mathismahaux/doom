import pygame as pg
from parametres import *

class MoteurRenduObjets:
    def __init__(self, j):
        self.jeu = j
        self.ecran = self.jeu.ecran
        self.textures_murs = self.charger_textures_murs()
        self.image_ciel = self.get_texture('ressources/textures/ciel.png', (LARG, DEMI_HAUT))
        self.decalage_ciel = 0

    def dessiner(self):
        self.dessiner_fond()
        self.rendre_objets()

    def dessiner_fond(self):
        self.decalage_ciel = (self.decalage_ciel + 4.5 * self.jeu.joueur.rel) % LARG
        self.ecran.blit(self.image_ciel, (-self.decalage_ciel, 0))
        self.ecran.blit(self.image_ciel, (-self.decalage_ciel + LARG, 0))
        pg.draw.rect(self.ecran, COULEUR_SOL, (0, DEMI_HAUT, LARG, HAUT))


    def rendre_objets(self):
        liste_objets = self.jeu.rc.objets_a_rendre
        liste_objets = sorted(self.jeu.rc.objets_a_rendre, key=lambda t: t[0], reverse=True)
        for prof, image, pos in liste_objets:
            self.ecran.blit(image, pos)

    @staticmethod
    def get_texture(chemin, res=(TAILLE_TEXTURE, TAILLE_TEXTURE)):
        texture = pg.image.load(chemin).convert_alpha()
        return pg.transform.scale(texture, res)

    def charger_textures_murs(self):
        return {
            1: self.get_texture('ressources/textures/m1.png'),
            2: self.get_texture('ressources/textures/m2.png')
        }
