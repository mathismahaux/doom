import pygame as pg
from parametres import *
import os
from collections import deque


class ObjetSprite:
    def __init__(self, j, c='ressources/sprites/statiques/chandelle.png', p=(10.5, 3.5), e=0.7, d=0.27):
        self.jeu = j
        self.joueur = j.joueur
        self.x, self.y = p
        self.image = pg.image.load(c).convert_alpha()
        self.LARG_IM = self.image.get_width()
        self.DEMI_LARG_IM = self.image.get_width() // 2
        self.RATIO_IM = self.LARG_IM / self.image.get_height()
        self.dx, self.dy, self.theta, self.x_ecran, self.dist, self.dist_norm = 0, 0, 0, 0, 1, 1
        self.demi_larg_sprite = 0
        self.ECHELLE_SPRITE = e
        self.DECALAGE_HAUTEUR_SPRITE = d

    def get_projection_sprite(self):
        proj = DIST_MUR / self.dist_norm * self.ECHELLE_SPRITE
        larg_proj, haut_proj = proj * self.RATIO_IM, proj

        image = pg.transform.scale(self.image, (larg_proj, haut_proj))

        self.demi_larg_sprite = larg_proj // 2
        dec_haut = haut_proj * self.DECALAGE_HAUTEUR_SPRITE
        pos = self.x_ecran - self.demi_larg_sprite, DEMI_HAUT - haut_proj // 2 + dec_haut

        self.jeu.rc.objets_a_rendre.append((self.dist_norm, image, pos))

    def get_sprite(self):
        dx = self.x - self.joueur.x
        dy = self.y - self.joueur.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.joueur.angle
        if(dx > 0 and self.joueur.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        d_rays = delta / D_ANGLE
        self.x_ecran = (DEMI_NB_RAYONS + d_rays) * ECHELLE

        self.dist = math.hypot(dx, dy)
        self.dist_norm = self.dist * math.cos(delta)
        if -self.DEMI_LARG_IM < self.x_ecran < (LARG + self.DEMI_LARG_IM) and self.dist_norm > 0.5:
            self.get_projection_sprite()

    def maj(self):
        self.get_sprite()

class SpriteAnime(ObjetSprite):
    def __init__(self, j, c='ressources/sprites/animes/flamme_verte/0.png', p=(11.5, 3.5), e=0.8, d=0.15, t_a=120):
        super().__init__(j, c, p, e, d)
        self.temps_animation = t_a
        self.chemin = c.rsplit('/', 1)[0]
        self.images = self.get_images(self.chemin)
        self.temps_animation_precedent = pg.time.get_ticks()
        self.declencheur_animation = False

    def maj(self):
        super().maj()
        self.verif_temps_animation()
        self.animer(self.images)

    def animer(self, images):
        if self.declencheur_animation:
            images.rotate(-1)
            self.image = images[0]

    def verif_temps_animation(self):
        self.declencheur_animation = False
        temps_actuel = pg.time.get_ticks()
        if temps_actuel - self.temps_animation_precedent > self.temps_animation:
            self.temps_animation_precedent = temps_actuel
            self.declencheur_animation = True

    def get_images(self, c):
        images = deque()
        for nom_fichier in os.listdir(c):
            if os.path.isfile(os.path.join(c, nom_fichier)):
                img = pg.image.load(c + '/' + nom_fichier).convert_alpha()
                images.append(img)
        return images

