from heapq import heappop, heappush
import math

class Graph:
    def __init__(self, directed=False):
        self._edges = dict()  # Dictionnaire pour stocker les arêtes
        self._isDirected = directed  # Booléen pour indiquer si le graphe est orienté

    def __len__(self):
        return len(self._edges)  # Retourne le nombre d'arêtes dans le graphe

    def __iter__(self):
        return iter(self._edges.keys())  # Permet l'itération sur les nœuds du graphe

    def __getitem__(self, node):
        return self._edges[node]  # Retourne les arêtes sortantes du nœud spécifié

    def add_node(self, s):
        if s not in self._edges:
            self._edges[s] = []  # Ajoute un nœud au graphe s'il n'existe pas déjà

    def add_edge(self, source, target, weight=None):
        self.add_node(source)  # Ajoute le nœud source s'il n'existe pas déjà
        self.add_node(target)  # Ajoute le nœud cible s'il n'existe pas déjà
        self._edges[source].append((target, weight))  # Ajoute une arête du nœud source au nœud cible avec un poids donné
        if not self._isDirected:
            self._edges[target].append((source, weight))  # Si le graphe n'est pas orienté, ajoute également une arête du nœud cible au nœud source

    def __str__(self):
        s = ""
        for (n, out) in self._edges.items():
            s += n.__str__() + " -> " + out.__str__() + "\n"  # Chaîne de caractères représentant le graphe
        return s

    def dfs_paths(self, start, end, path=[]):
        if path is None:
            path = []  # Si le chemin est None, on initialise avec une liste vide
        path.append(start)  # On ajoute le nœud de départ au chemin
        if start == end:
            return [path]  # Si on atteint le nœud de destination, on retourne le chemin trouvé
        if start not in self._edges:
            return []  # Si le nœud de départ n'est pas dans le graphe, il n'y a pas de chemin possible
        paths = []  # Liste pour stocker les chemins possibles
        visited = set(path)  # Ensemble pour stocker les nœuds déjà visités
        for (node, k) in self._edges[start]:
            if node not in visited:
                new_paths = self.dfs_paths(node, end, path[:])  # Appel récursif pour continuer le parcours
                paths.extend(new_paths)  # Ajout des nouveaux chemins trouvés à la liste des chemins
                visited.add(node)  # Ajout du nœud visité à l'ensemble des nœuds visités
        print(path)  # Affichage du chemin parcouru (facultatif)
        return paths  # Retourne tous les chemins possibles


    def trajet_possible(self, start, end):
        paths = self.dfs_paths(start, end)  # Appel de la méthode dfs_paths pour trouver tous les chemins possibles
        return paths  # Retourne les chemins possibles


    def bellman_ford(self, start, destination, graph=None):
        dist = dict()  # Dictionnaire pour stocker les distances
        pred = dict()  # Dictionnaire pour stocker les prédécesseurs

        for n in self:
            dist[n] = math.inf  # Initialise toutes les distances à l'infini
            pred[n] = None  # Initialise tous les prédécesseurs à None
        dist[start] = 0  # La distance du nœud de départ est de 0

        if graph == None:
            graph = self._edges 
        else:
            graph = graph

        for k in range(0, len(self) - 1):
            for u in graph:
                for (v, w) in self[u]:
                    if dist[v] > dist[u] + w:  # Si la distance actuelle est supérieure à la distance par le nouveau chemin
                        dist[v] = dist[u] + w  # Met à jour la distance
                        pred[v] = u  # Met à jour le prédécesseur

        # Vérification de la présence d'un cycle négatif
        for u in graph:
            for (v, w) in self[u]:
                if dist[v] > dist[u] + w:  # S'il y a encore une amélioration, il y a un cycle négatif
                    return None
        # Retourne le chemin et la distance
        path = [destination]  # Initialise le chemin avec le nœud de destination
        node = destination  # Commence à partir du nœud de destination
        while pred[node] is not None:
            path.append(pred[node])  # Ajoute le prédécesseur au chemin
            node = pred[node]  # Met à jour le nœud courant
        path.reverse()  # Inverse le chemin pour l'ordre correct

        return [path, dist[destination]] # Retourne le chemin et la distance

if __name__ == "__main__":
    G = Graph()
    G.add_edge("s", "a", 10)
    G.add_edge("s", "e", 5)
    G.add_edge("e", "d", 12) 
    G.add_edge("d", "a", 7)
    G.add_edge("d", "c", 6)
    G.add_edge("c", "b", 6)
    G.add_edge("b", "a", 9)
    G.add_edge("a", "c", 2)
