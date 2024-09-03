from objet_sprite import *

class Arme(SpriteAnime):
    def __init__(self, j, c='ressources/sprites/arme/shotgun/0.png', e=0.4, t_a=90):
        super().__init__(j=j, c=c, e=e, t_a=t_a)
        self.images = deque([pg.transform.smoothscale(i, (self.image.get_width() * e, self.image.get_height() * e)) for i in self.images])
        self.pos_arme = (DEMI_LARG - self.images[0].get_width() // 2, HAUT - self.images[0].get_height())
        self.recharge = False
        self.nb_images = len(self.images)
        self.compteur_frames = 0
        self.degats = 50

    def animer_tir(self):
        if self.recharge:
            self.jeu.joueur.tir = False
            if self.declencheur_animation:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.compteur_frames += 1
                if self.compteur_frames == self.nb_images:
                    self.recharge = False
                    self.compteur_frames = 0

    def dessiner(self):
        self.jeu.ecran.blit(self.images[0], self.pos_arme)

    def maj(self):
        self.verif_temps_animation()
        self.animer_tir()
