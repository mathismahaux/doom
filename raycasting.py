import pygame as pg
import math
from parametres import *

class RayCasting:
    def __init__(self, j):
        self.jeu = j
        self.resultat_raycasting = []
        self.objets_a_rendre = []
        self.textures = self.jeu.mro.textures_murs

    def get_objets_a_rendre(self):
        self.objets_a_rendre = []
        for ray, valeurs in enumerate(self.resultat_raycasting):
            prof, haut_proj, texture, decalage = valeurs

            if haut_proj < HAUT:
                colonne_mur = self.textures[texture].subsurface(
                    decalage * (TAILLE_TEXTURE - ECHELLE), 0, ECHELLE, TAILLE_TEXTURE
                )
                colonne_mur = pg.transform.scale(colonne_mur, (ECHELLE, haut_proj))
                pos_mur = (ray * ECHELLE, DEMI_HAUT - haut_proj // 2)
            else:
                haut_texture = TAILLE_TEXTURE * HAUT / haut_proj
                colonne_mur = self.textures[texture].subsurface(
                    decalage * (TAILLE_TEXTURE - ECHELLE), DEMI_TAILLE_TEXTURE - haut_texture // 2, ECHELLE, haut_texture
                )
                colonne_mur = pg.transform.scale(colonne_mur, (ECHELLE, HAUT))
                pos_mur = (ray * ECHELLE, 0)

            self.objets_a_rendre.append((prof, colonne_mur, pos_mur))

    def ray_cast(self):
        self.resultat_raycasting = []
        jx, jy = self.jeu.joueur.pos
        x_carte, y_carte = self.jeu.joueur.carte_pos
        texture_vert, texture_hor = 1, 1
        angle_ray = self.jeu.joueur.angle - DEMI_FOV + 0.0001
        for ray in range(NB_RAYONS):
            angle_ray += D_ANGLE
            sin_a = math.sin(angle_ray)
            cos_a = math.cos(angle_ray)

            y_hor, dy = (y_carte + 1, 1) if sin_a > 0 else (y_carte - 1e-6, -1)
            prof_hor = (y_hor - jy) / sin_a
            x_hor = jx + prof_hor * cos_a
            d_prof = dy / sin_a
            dx = d_prof * cos_a

            for i in range(PROF_MAX):
                tuile_hor = int(x_hor), int(y_hor)
                if tuile_hor in self.jeu.carte.carte_monde:
                    texture_hor = self.jeu.carte.carte_monde[tuile_hor]
                    break
                x_hor += dx
                y_hor += dy
                prof_hor += d_prof

            x_vert, dx = (x_carte + 1, 1) if cos_a > 0 else (x_carte - 1e-6, -1)
            prof_vert = (x_vert - jx) / cos_a
            y_vert = jy + prof_vert * sin_a
            d_prof = dx / cos_a
            dy = d_prof * sin_a

            for i in range(PROF_MAX):
                tuile_vert = int(x_vert), int(y_vert)
                if tuile_vert in self.jeu.carte.carte_monde:
                    texture_vert = self.jeu.carte.carte_monde[tuile_vert]
                    break
                x_vert += dx
                y_vert += dy
                prof_vert += d_prof

            if prof_vert < prof_hor:
                prof, texture = prof_vert, texture_vert
                y_vert %= 1
                decalage = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                prof, texture = prof_hor, texture_hor
                x_hor %= 1
                decalage = (1 - x_hor) if sin_a > 0 else x_hor

            #Retire l'effet "Fisheye"
            prof *= math.cos(self.jeu.joueur.angle - angle_ray)

            haut_proj = DIST_MUR / (prof + 0.0001)

            self.resultat_raycasting.append((prof, haut_proj, texture, decalage))

            # couleur = [255 / (1 + prof ** 5 * 0.00002)] * 3
            # pg.draw.rect(self.jeu.ecran, couleur, (ray * ECHELLE, DEMI_HAUT - haut_proj // 2, ECHELLE, haut_proj))

    def maj(self):
        self.ray_cast()
        self.get_objets_a_rendre()

