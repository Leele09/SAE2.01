from Graph import Graph

#import pour le bonus tout en bas :
from queue import PriorityQueue
from relation import *
import pandas as pd
import copy

class metro():
    def __init__(self):
        self.station = []    # Liste des stations du métro
        self.relation = []   # Liste des relations entre les stations
        self.graph = Graph()
        self.color_line = {"1": "#FFCE00", "2": "#0064B0", "3": "#9F9825", "4": "#C04191", "5": "#F28E42",
                           "6": "#83C491", "7": "#F3A4BA", "8": "#CEADD2", "9": "#D5C900", "10": "#E3B32A",
                           "11": "#8D5E2A", "12": "#00814F", "13": "#98D4E2", "14": "#662483", "3b": "#98D4E2",
                           "7b": "#83C491"}

    def add_station(self, station):
        self.station.append(station)   # Ajouter une station à la liste des stations
    
    def add_relation(self, relation):
        self.relation.append(relation)   # Ajouter une relation à la liste des relations

    def construire_graph(self):
        # INSERTION DES STATIONS ET DES RELATIONS DANS LE RESEAU
        for relation in self.relation:
            self.graph.add_edge(relation.id1, relation.id2, relation.temps)
    
    def get_stations_of_line(self , line):
        lst_station = [i.nom for i in self.station if line == i.ligne]   # Liste des noms des stations appartenant à une ligne spécifiée
        return lst_station
    
    def get_stations_obj_of_line(self , line):
        lst_station = [i for i in self.station if line == i.ligne]   # Liste des noms des stations appartenant à une ligne spécifiée
        return lst_station

    def correspondance(self, line1, line2):
        # Retourner les stations qui sont des correspondances entre deux lignes spécifiées
        return list(set(self.get_stations_of_line(line1)) & set(self.get_stations_of_line(line2)))
    
    def correspondance_obj(self, line1, line2):
        # Retourner les stations qui sont des correspondances entre deux lignes spécifiées
        lst_correspondance_obj = []
        lst_station_line1 = self.get_stations_obj_of_line(line1)
        lst_station_line2 = self.get_stations_obj_of_line(line2)

        # Boucle qui permet de vérifier de remplir la variable avec les correspondances
        for station in lst_station_line1:
            for station2 in lst_station_line2:
                if station.nom == station2.nom:
                    lst_correspondance_obj.append(station)
        return lst_correspondance_obj
    
    def stations_proches(self, station):
        # Va prendre les stations en relation avec la station rentré
        return [x[0] for x in self.graph._edges[station]]

    def trajet_possible(self, start, end):
        # variable qui va stocker les différents chemins
        paths = []

        # On crée une copie du graph 
        graph = Graph()
        for relation in self.relation:
            graph.add_edge(relation.id1, relation.id2, relation.temps)
        graph_base = copy.deepcopy(graph)

        # On crée une variable qui va servir a parcourir les stations retourné par bellman ford
        index = 0
        while len(paths)<5:
            nbr_correspondance = 0
            lst_line_color = []
            try:
                # On va à chaque fois faire appel à bellmanford en lui passant différent graphique
                chemin = graph_base.bellman_ford(start,end,graph)
                # Ceci permet de modifier les élements renvoyé par bellmanford en str pour plus tard
                chemin_str = [[str(i) for i in chemin[0]] , str(chemin[1])]
                graph = graph_base
                # Ici on parcours le résultat et on enléve une arete
                for i in graph[chemin[0][index]]:
                    if i[0] == chemin[0][chemin[0].index(chemin[0][index])+1]:
                        graph[chemin[0][index]].remove(i)
                        break
                index += 1
                chemin_str.append(str(len(chemin[0])))

                # Ici on traite le compteur pour avoir le nombre de corrspondances
                for i in range(len(chemin[0])-1):
                    station_before = None
                    station_after = None
                    # Cette boucle la permet de transformer les élements du chemin retourné en objet station
                    for station_obj in self.station:
                        if station_obj.id == chemin[0][i]:
                            station_before = station_obj
                        elif station_obj.id == chemin[0][i+1]:
                            station_after = station_obj
                            lst_line_color.append(self.color_line[station_after.ligne])
                    # Si la ligne de la station actuelle est différente de la ligne de la prochaine station alors il y a une correspindace
                    if station_before.ligne != station_after.ligne:
                        nbr_correspondance +=1
                chemin_str.append(str(nbr_correspondance))
                chemin_str.append(lst_line_color)
                paths.append(chemin_str)
            # Si on catch d'index alors on suppose qu'il n'y plus de chemin 
            except IndexError:
                return paths
        self.graph = graph_base
        return paths


    def trajet_station_tiers(self,  station_depart , station_tiers, station_fin):
        # On fait un bellmanford de la station 1 à la station tiers et ensuite de la station tiers à la station 2
        etapes1, temps1 = self.graph.bellman_ford(station_depart,station_tiers)
        etapes2, temps2 = self.graph.bellman_ford(station_tiers, station_fin)
        # On enléve la première station du deuxième résultat vu que c'est la même que la dernière du premier résultat
        etapes2.remove(etapes2[0])

        # Et on renvoie les deux résultats assemblés
        return (etapes1+etapes2),temps1+temps2
    
    def reliees_p_distance(self, station1, station2, distance):
        # On fait bellmanford sur les deux stations en argument
        chemin = self.graph.bellman_ford(station1, station2)

        result = []
        # Pour commencer on ajoute au resultat true si la distance retourné par bellmanford est inférieur ou égale à la distance rentré par l'utilisateur
        # Sinon false
        if  chemin[1] <= distance:
            result.append(True)
        else:
            result.append(False)
        # Dans le résultat on ajoute ensuite le résultat de bellmanford changé en str pour plus tard
        result.append([[str(station) for station in chemin[0]], str(chemin[1])])

        colors = []

        # Cette boucle permet de récupérer les couleurs des lignes des aretes emprunté
        for station1 in range(len(chemin[0]) -1 ):
            for station_obj in self.station:
                if chemin[0][station1] == station_obj.id:
                    for indice in self.graph[station_obj.id]:
                        if indice[0] == chemin[0][station1+1]:
                            tps= indice[1]
                            break
                    colors.append((self.color_line[station_obj.ligne], str(tps)))
        # Et on ajoute aussi à résultat
        result.append(colors)
        return result

    def plus_accessible(self, station1_id, station2_id , p_distance):
        stations = pd.DataFrame(pd.read_csv("Données/stations.csv", sep=";"))

        # On récupère les objets des stations vie leurs id 
        for station in self.station:
            if station.id == station1_id:
                station1_obj = station
            elif station.id == station2_id:
                station2_obj = station

            # Variables
        lst_correspondance_of_station1_line = []
        lst_correspondance_of_station2_line = []
        lst_ligne = [ligne for ligne in set(stations["ligne"])]
        lst_terminale = [station for station in self.station if station.terminus == 1]


        # On remplie la liste de correspondance de la ligne de la station 1 et 2
        for line in lst_ligne:
            temp1 = self.correspondance_obj(station1_obj.ligne , line)
            temp2= self.correspondance_obj(station2_obj.ligne , line)

            for correspondance1 in temp1:
                if correspondance1 not in lst_correspondance_of_station1_line:
                    lst_correspondance_of_station1_line.append(correspondance1)

            for correspondance2 in temp2:
                if correspondance2 not in lst_correspondance_of_station2_line:
                    lst_correspondance_of_station2_line.append(correspondance2)

            	        # ANALYSE
        # ACCESSIBLE
        distance_min_station1_correspondance = None      
        distance_min_station2_correspondance = None
        # CENTRALE
        station1_correspondance_p_distance = 0
        station2_correspondance_p_distance = 0
        # TERMINALE
        distance_min_station1_terminus = None      
        distance_min_station2_terminus = None

                            # Analyse Accessible et Central
        # On trouve la distance minimale de la station1 vers une correspondance 
        for correspondance1 in lst_correspondance_of_station1_line:
            if station1_id != correspondance1.id:
                distance = self.graph.bellman_ford(station1_id , correspondance1.id)
                # On vérifie l'accéssibilité
                if distance_min_station1_correspondance is None:
                    distance_min_station1_correspondance = distance
                else:
                    if distance[1] < distance_min_station1_correspondance[1]:
                        distance_min_station1_correspondance = distance
                # On vérifie la centralité
                if distance[1] <= p_distance:
                    station1_correspondance_p_distance +=1

        # On trouve la distance minimale de la station2 vers une correspondance
        for correspondance2 in lst_correspondance_of_station2_line:
            if station2_id != correspondance2.id:
                distance = self.graph.bellman_ford(station2_id , correspondance2.id)

                # On vérifie l'accéssibilité
                if distance_min_station2_correspondance is None:
                    distance_min_station2_correspondance = distance
                else:
                    if distance[1] < distance_min_station2_correspondance[1]:
                        distance_min_station2_correspondance = distance 
                # On vérifie la centralité
                if distance[1] <= p_distance:
                    station2_correspondance_p_distance +=1

                            # Analyse Terminale
        # On trouve la distance minimale de la station1 vers un terminus
        for terminus in lst_terminale:
            distance1 = self.graph.bellman_ford(station1_id , terminus.id)
            distance2 = self.graph.bellman_ford(station2_id , terminus.id)

            # On vérifie l'accéssibilité
            if distance_min_station1_terminus is None:
                distance_min_station1_terminus = distance1
            else:
                if distance1[1] < distance_min_station1_terminus[1]:
                    distance_min_station1_terminus = distance1

            # On vérifie l'accéssibilité
            if distance_min_station2_terminus is None:
                distance_min_station2_terminus = distance2
            else:
                if distance2[1] < distance_min_station2_terminus[1]:
                    distance_min_station2_terminus = distance2

        # Liste qui va contenir les valeurs à renvvoye
        reponse = []

        # Réponse ACCESSIBLE
        lst_color_correspondance = []
        lst_color_terminus = []
        if distance_min_station1_correspondance[1] < distance_min_station2_correspondance[1]:
            # Change station id with their object
            for station_id in distance_min_station1_correspondance[0]:
                for station_obj in self.station:
                    if station_id == station_obj.id:
                        lst_color_correspondance.append(self.color_line[station_obj.ligne])
            reponse.append([f"La station {station1_id} est plus proche d'une correspondance que la {station2_id} : {distance_min_station1_correspondance[1]} contre {distance_min_station2_correspondance[1]}", [str(i) for i in distance_min_station1_correspondance[0]],lst_color_correspondance[1:]])
        elif distance_min_station1_correspondance[1] > distance_min_station2_correspondance[1]:
            # Change station id with their object
            for station_id in distance_min_station2_correspondance[0]:
                for station_obj in self.station:
                    if station_id == station_obj.id:
                        lst_color_correspondance.append(self.color_line[station_obj.ligne])
            reponse.append([f"La station {station2_id} est plus proche d'une correspondance que la {station1_id} : {distance_min_station2_correspondance[1]} contre {distance_min_station1_correspondance[1]}", [str(i) for i in distance_min_station2_correspondance[0]],lst_color_correspondance[1:]])
        else:
            reponse.append([f"Les stations {station1_id} et {station2_id} sont à égal distance par rapport à une correspondance : {distance_min_station1_correspondance[1]}"])

        # Réponse CENTRALE 
        if station1_correspondance_p_distance > station2_correspondance_p_distance:
            reponse.append(f"La station {station1_id} est plus centrale que la {station2_id} : {station1_correspondance_p_distance} contre {station2_correspondance_p_distance}")
        elif station1_correspondance_p_distance < station2_correspondance_p_distance:
            reponse.append(f"La station {station2_id} est plus centrale que la {station1_id} : {station2_correspondance_p_distance} contre {station1_correspondance_p_distance}")
        else:
            reponse.append(f"Les stations {station1_id} et {station2_id} sont aussi centrale l'un que l'autre : {station1_correspondance_p_distance}")

        # Réponse TERMINALE 
        if distance_min_station1_terminus[1] < distance_min_station2_terminus[1]:
            # Change station id with their object
            for station_id in distance_min_station1_terminus[0]:
                for station_obj in self.station:
                    if station_id == station_obj.id:
                        lst_color_terminus.append(self.color_line[station_obj.ligne])
            reponse.append([f"La station {station1_id} est plus plus proche d'un terminus que la {station2_id} : {distance_min_station1_terminus[1]} contre {distance_min_station2_terminus[1]}", [str(i) for i in distance_min_station1_terminus[0]],lst_color_terminus[1:]])
        elif distance_min_station1_terminus[1] > distance_min_station2_terminus[1]:
            # Change station id with their object
            for station_id in distance_min_station2_terminus[0]:
                for station_obj in self.station:
                    if station_id == station_obj.id:
                        lst_color_terminus.append(self.color_line[station_obj.ligne])
            reponse.append([f"La station {station2_id} est plus plus proche d'un terminus que la {station1_id} : {distance_min_station2_terminus[1]} contre {distance_min_station1_terminus[1]}", [str(i) for i in distance_min_station2_terminus[0]],lst_color_terminus[1:]] )
        else:
            reponse.append([f"Les stations {station1_id} et {station2_id} sont aussi terminale l'un que l'autre : {distance_min_station1_terminus[1]}"])
        
        return reponse


    #########                           #########
    ################    BONUS    ################
    #########                           #########

    def acm(self):
        # Créer un dictionnaire pour stocker les sommets et leurs voisins avec les poids des arêtes
        graph_dict = {}
        for relation in self.relation:
            id1 = relation.id1
            id2 = relation.id2
            temps = relation.temps

            if id1 not in graph_dict:
                graph_dict[id1] = {}
            if id2 not in graph_dict:
                graph_dict[id2] = {}

            graph_dict[id1][id2] = temps
            graph_dict[id2][id1] = temps

        # Créer une file de priorité pour stocker les arêtes selon leurs poids
        priority_queue = PriorityQueue()

        # Choisir un sommet de départ arbitraire
        start_vertex = self.station[0].id

        # Initialiser un dictionnaire pour suivre les sommets visités
        visited = {start_vertex}

        # Ajouter les arêtes adjacentes du sommet de départ à la file de priorité
        for neighbor, weight in graph_dict[start_vertex].items():
            priority_queue.put((weight, start_vertex, neighbor))

        # Initialiser un dictionnaire pour stocker l'arbre de recouvrement minimum
        minimum_spanning_tree = {}

        # Itérer jusqu'à ce que tous les sommets soient visités ou la file de priorité est vide
        while not priority_queue.empty():
            # Extraire l'arête avec le poids minimum de la file de priorité
            weight, vertex1, vertex2 = priority_queue.get()

            if vertex2 not in visited:
                # Ajouter l'arête à l'arbre de recouvrement minimum
                if vertex1 not in minimum_spanning_tree:
                    minimum_spanning_tree[vertex1] = {}
                minimum_spanning_tree[vertex1][vertex2] = weight

                # Marquer le sommet comme visité
                visited.add(vertex2)

                # Ajouter les arêtes adjacentes du sommet visité à la file de priorité
                for neighbor, weight in graph_dict[vertex2].items():
                    if neighbor not in visited:
                        priority_queue.put((weight, vertex2, neighbor))

        # Mettre à jour les relations avec l'arbre de recouvrement minimum
        relation_acm = []
        for vertex1, neighbors in minimum_spanning_tree.items():
            for vertex2, weight in neighbors.items():
                relation_acm.append(Relation(vertex1, vertex2, weight))

        return relation_acm
