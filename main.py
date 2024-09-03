import pygame as pg
import sys
from parametres import *
from carte import *
from joueur import *
from raycasting import *
from moteur_rendu_objets import *
from objet_sprite import *
from gestion_objets import *
from arme import *
from pathfinding import *

class Jeu:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.ecran = pg.display.set_mode(RES)
        self.horloge = pg.time.Clock()
        self.dt = 1
        self.declencheur_global = False
        self.evenement_global = pg.USEREVENT + 0
        pg.time.set_timer(self.evenement_global, 40)
        self.nouveau_jeu()

    def nouveau_jeu(self):
        self.carte = Carte(self)
        self.joueur = Joueur(self)
        self.mro = MoteurRenduObjets(self)
        self.rc = RayCasting(self)
        self.ss = ObjetSprite(self)
        self.ans = SpriteAnime(self)
        self.go = GestionObjets(self)
        self.a = Arme(self)
        self.pf = Pathfinding(self)

    def maj(self):
        self.joueur.maj()
        self.rc.maj()
        self.ss.maj()
        self.ans.maj()
        self.go.maj()
        self.a.maj()
        pg.display.flip()
        self.dt = self.horloge.tick(FPS)
        pg.display.set_caption(f'{self.horloge.get_fps():.1f}')

    def dessine(self):
        # self.ecran.fill('black')
        self.mro.dessiner()
        self.a.dessiner()
        # self.carte.dessiner()
        # self.joueur.dessiner()

    def chequer_evenements(self):
        self.declencheur_global = False
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif e.type == self.evenement_global:
                self.declencheur_global = True
            self.joueur.evenement_tir_unique(e)

    def execute(self):
        while True:
            self.chequer_evenements()
            self.maj()
            self.dessine()

if __name__ == '__main__':
    j = Jeu()
    j.execute()
