from collections import deque

class Pathfinding:
    def __init__(self, j):
        self.jeu = j
        self.carte = j.carte.mini_carte
        self.chemins = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self.get_graph()

    def get_chemin(self, debut, but):
        self.visite = self.bfs(debut, but, self.graph)
        chemin = [but]
        etape = self.visite.get(but, debut)

        while etape and etape != debut:
            chemin.append(etape)
            etape = self.visite[etape]

        return chemin[-1]

    #Algorithme "Breadth first search"
    def bfs(selfself, debut, but, graph):
        queue = deque([debut])
        visite = {debut: None}

        while queue:
            noeud_courant = queue.popleft()
            if noeud_courant == but:
                break
            noeuds_suiv = graph[noeud_courant]

            for noeud_suiv in noeuds_suiv:
                if noeud_suiv not in visite:
                    queue.append(noeud_suiv)
                    visite[noeud_suiv] = noeud_courant
        return visite

    def get_noeuds_suiv(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.chemins if (x + dx, y + dy) not in self.jeu.carte.carte_monde]


    def get_graph(self):
        for y, ligne in enumerate(self.carte):
            for x, colonne in enumerate(ligne):
                if not colonne:
                    self.graph[(x, y)] = self.graph.get((x, y), []) +self.get_noeuds_suiv(x, y)
