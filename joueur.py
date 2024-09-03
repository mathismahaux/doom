from parametres import *
import pygame as pg
import math


class Joueur:
    def __init__(self, j):
        self.jeu = j
        self.x, self.y = POS_JOUEUR
        self.angle = ANGLE_JOUEUR
        self.tir = False

    def evenement_tir_unique(self, e):
        if e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1 and not self.tir and not self.jeu.a.recharge:
                self.tir = True
                self.jeu.a.recharge = True

    def bouger(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        vitesse = VITESSE_JOUEUR * self.jeu.dt
        sin_vit = vitesse * sin_a
        cos_vit = vitesse * cos_a

        touches = pg.key.get_pressed()
        if touches[pg.K_z]:
            dx += cos_vit
            dy += sin_vit
        if touches[pg.K_s]:
            dx += -cos_vit
            dy += -sin_vit
        if touches[pg.K_q]:
            dx += sin_vit
            dy += -cos_vit
        if touches[pg.K_d]:
            dx += -sin_vit
            dy += cos_vit

        # self.x += dx
        # self.y += dy
        self.chequer_collision_murs(dx, dy)

        # if touches[pg.K_LEFT]:
        #     self.angle -= VITESSE_ROT_JOUEUR * self.jeu.dt
        # if touches[pg.K_RIGHT]:
        #     self.angle += VITESSE_ROT_JOUEUR * self.jeu.dt
        self.angle %= math.tau

    def chequer_murs(self, x, y):
        return (x, y) not in self.jeu.carte.carte_monde

    def chequer_collision_murs(self, dx, dy):
        echelle = TAILLE_JOUEUR / self.jeu.dt
        if self.chequer_murs(int(self.x + dx * echelle), int(self.y)):
            self.x += dx
        if self.chequer_murs(int(self.x), int(self.y + dy * echelle)):
            self.y += dy

    def dessiner(self):
        pg.draw.circle(self.jeu.ecran, 'green', (self.x * 100, self.y * 100), 15)

        # pg.draw.line(self.jeu.ecran, 'red', (self.x * 100, self.y * 100),
        #              (self.x * 100 + LARG * math.cos(self.angle),
        #               self.y * 100 + LARG * math.sin(self.angle)), 2)

    def ctrl_souris(self):
        sx, sy = pg.mouse.get_pos()
        if sx < BORDURE_GAUCHE_SOURIS or sx > BORDURE_DROITE_SOURIS:
            pg.mouse.set_pos([DEMI_LARG, DEMI_HAUT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MVT_REL_MAX_SOURIS, min(MVT_REL_MAX_SOURIS, self.rel))
        self.angle += self.rel * SENSIBILITE_SOURIS * self.jeu.dt

    def maj(self):
        self.bouger()
        self.ctrl_souris()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def carte_pos(self):
        return int(self.x), int(self.y)
