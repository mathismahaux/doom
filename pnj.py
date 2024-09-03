from objet_sprite import *
from random import randint, random, choice

class Pnj(SpriteAnime):
    def __init__(self, j, c='ressources/sprites/pnj/soldat/0.png', p=(10.5, 5.5),
                 e=0.6, d=0.38, t_a=180):
        super().__init__(j, c, p, e, d, t_a)
        self.images_attaque = self.get_images(self.chemin + '/attaque')
        self.images_mort = self.get_images(self.chemin + '/mort')
        self.images_debout = self.get_images(self.chemin + '/debout')
        self.images_douleur = self.get_images(self.chemin + '/douleur')
        self.images_marche = self.get_images(self.chemin + '/marche')

        self.dist_attaque = randint(3, 6)
        self.vitesse = 0.03
        self.taille = 10
        self.sante = 100
        self.degats = 10
        self.precision = 0.15
        self.vivant = True
        self.douleur = False
        self.valeur_raycasting = False
        self.compteur_frames = 0
        self.declencheur_recherche_joueur = False

    def maj(self):
        self.verif_temps_animation()
        self.get_sprite()
        self.logique()
        # self.dessiner_raycasting()

    def chequer_murs(self, x, y):
        return (x, y) not in self.jeu.carte.carte_monde

    def chequer_collision_murs(self, dx, dy):
        if self.chequer_murs(int(self.x + dx * self.taille), int(self.y)):
            self.x += dx
        if self.chequer_murs(int(self.x), int(self.y + dy * self.taille)):
            self.y += dy

    def mouvement(self):
        pos_suiv = self.jeu.pf.get_chemin(self.carte_pos, self.jeu.joueur.carte_pos)
        x_suiv, y_suiv = pos_suiv
        # pg.draw.rect(self.jeu.ecran, 'blue', (100 * x_suiv, 100 * y_suiv, 100, 100))
        angle = math.atan2(y_suiv + 0.5 - self.y, x_suiv + 0.5 - self.x)
        dx = math.cos(angle) * self.vitesse
        dy = math.sin(angle) * self.vitesse
        self.chequer_collision_murs(dx, dy)

    def animer_mort(self):
        if not self.vivant:
            if self.jeu.declencheur_global and self.compteur_frames < len(self.images_mort) - 1:
                self.images_mort.rotate(-1)
                self.image = self.images_mort[0]
                self.compteur_frames += 1


    def animer_douleur(self):
        self.animer(self.images_douleur)
        if self.declencheur_animation:
            self.douleur = False

    def verif_coup_dans_pnj(self):
        if self.valeur_raycasting and self.jeu.joueur.tir:
            if DEMI_LARG - self.demi_larg_sprite < self.x_ecran < DEMI_LARG + self.demi_larg_sprite:
                self.jeu.joueur.tir = False
                self.douleur = True
                self.sante -= 50
                self.verif_sante()

    def verif_sante(self):
        if self.sante < 1:
            self.vivant = False

    def logique(self):
        if self.vivant:
            self.valeur_raycasting = self.ray_cast_joueur_pnj()
            self.verif_coup_dans_pnj()
            if self.douleur:
                self.animer_douleur()
            elif self.valeur_raycasting:
                self.declencheur_recherche_joueur = True
                self.animer(self.images_marche)
                self.mouvement()
            elif self.declencheur_recherche_joueur:
                self.animer(self.images_marche)
                self.mouvement()
            else:
                self.animer(self.images_debout)
        else:
            self.animer_mort()

    @property
    def carte_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_joueur_pnj(self):
        if self.jeu.joueur.carte_pos == self.carte_pos:
            return True

        dist_mur_v, dist_mur_h = 0, 0
        dist_joueur_v, dist_joueur_h = 0, 0

        jx, jy = self.jeu.joueur.pos
        x_carte, y_carte = self.jeu.joueur.carte_pos
        angle_ray = self.theta
        sin_a = math.sin(angle_ray)
        cos_a = math.cos(angle_ray)

        y_hor, dy = (y_carte + 1, 1) if sin_a > 0 else (y_carte - 1e-6, -1)
        prof_hor = (y_hor - jy) / sin_a
        x_hor = jx + prof_hor * cos_a
        d_prof = dy / sin_a
        dx = d_prof * cos_a

        for i in range(PROF_MAX):
            tuile_hor = int(x_hor), int(y_hor)
            if tuile_hor == self.carte_pos:
                dist_joueur_h = prof_hor
                break
            if tuile_hor in self.jeu.carte.carte_monde:
                dist_mur_h = prof_hor
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
            if tuile_vert == self.carte_pos:
                dist_joueur_v = prof_vert
                break
            if tuile_vert in self.jeu.carte.carte_monde:
                dist_mur_v = prof_vert
                break
            x_vert += dx
            y_vert += dy
            prof_vert += d_prof

        dist_joueur = max(dist_joueur_v, dist_joueur_h)
        dist_mur = max(dist_mur_v, dist_mur_h)

        if 0 < dist_joueur < dist_mur or not dist_mur:
            return True
        return False

    def dessiner_raycasting(self):
        pg.draw.circle(self.jeu.ecran, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_joueur_pnj():
            pg.draw.line(self.jeu.ecran, 'orange', (100 * self.jeu.joueur.x, 100 * self.jeu.joueur.y),
                         (100 * self.x, 100 * self.y), 2)
