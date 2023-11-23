import folium as fo
from folium.plugins import *
from metro import metro

class Map(metro):
    def __init__(self, liste_station, liste_ligne):
        self.liste_station = liste_station
        self.liste_ligne = liste_ligne

        # On initiaise la map à la création de l'objet
        self.zone_map = fo.Map(location=[48.856614, 2.34000], zoom_start=13)
        self.layer_ligne = {self.liste_ligne[line]: fo.FeatureGroup(name=f'Ligne: {self.liste_ligne[line]}', show=True)
                            for line in range(len(self.liste_ligne))}
        for line, layer in self.layer_ligne.items():
            self.zone_map.add_child(layer)
        metro.__init__(self)

        # On associe les lignes à des couleurs
        self.color_line = {"1": "#FFCE00", "2": "#0064B0", "3": "#9F9825", "4": "#C04191", "5": "#F28E42",
                           "6": "#83C491", "7": "#F3A4BA", "8": "#CEADD2", "9": "#D5C900", "10": "#E3B32A",
                           "11": "#8D5E2A", "12": "#00814F", "13": "#98D4E2", "14": "#662483", "3b": "#98D4E2",
                           "7b": "#83C491"}
        
        # Ajout d'une légende
        self.legend_html = '''
                <div style="position: fixed; 
                bottom: 40px; left: 35px; width: 250px; height: fit-content; padding:10px;
                border:2px solid black; z-index:9999; font-size:14px; border-radius:5px;
                background-color: rgba(0, 132, 255, 0.5);">
                <div style="position: absolute; top: -30px; left: 0; width: 100%; text-align:center;margin: -5px , 0"></div>
                    <div style="text-align:center;font-weight:bold;color:white">LÉGENDE </div>
                    &nbsp; <i class="fa-solid fa-train-subway"  style="color:white ;background-color:red ;padding:4px; border-radius:5px"></i>
                    <span style="color: black;"> Terminus </span> <br>
                    &nbsp; <i class="fa fa-circle" style="color:black" &nspb></i>
                    <span style="color: black;"> Station </span> <br>
                    &nbsp; <i class="fa fa-circle" style="color:white" &nspb></i>
                    <span style="color: black;"> Correspondance </span>
                </div>
                '''
        self.zone_map.get_root().html.add_child(fo.Element(self.legend_html))

                # Ajout des plugins 
        # Barre de recherche
        Geocoder(position='topleft').add_to(self.zone_map)
        # Pouvoir dessiner ses propres figures
        Draw(export=False,
             filename='dessin.geojson',
             position='topleft').add_to(self.zone_map)
        # Avoir sa localisation
        LocateControl().add_to(self.zone_map)
        # Avoir une minimap
        minimap = MiniMap(width=200)
        self.zone_map.add_child(minimap)
        # Mouse position
        MousePosition(position="bottomleft").add_to(self.zone_map)


    # Fonction qui place les marqueurs (station) sur la map
    def draw_marker(self, metro_obj, lst_ligne=None):
        # Création d'une carte folium avec une localisation et un niveau de zoom
        bordure_css = "style='border: 1px solid;'"
        lst_station_correspondance = []

        # Boucle qui cherche les correspondances dans la liste de ligne en argument
        if lst_ligne is not None:
            for i in range(len(lst_ligne)):
                for j in range(i + 1, len(lst_ligne)):
                    # On trouve les correspondances entre la ligne en cours et les pochaines lignes
                    temp = metro_obj.correspondance(lst_ligne[i], lst_ligne[j])
                    for name_station in temp:
                        if name_station not in lst_station_correspondance:
                            # On ajoutes dans une liste les station où il y a correspondance
                            lst_station_correspondance.append(name_station)

        for station in self.liste_station:
            if lst_ligne is not None:
                if station.ligne in lst_ligne:  # Si la station fait partit de la liste des lignes selectionné
                    opacity = 1
                    fill_opacity = 1
                    if station.nom in lst_station_correspondance:  # Et si il fait partit des stations correspondance
                        radius = 4
                        color = "white"
                    else:   # Fait juste partit de la ligne
                        radius = 3
                        color = "black"
                else: # On met les autres station en transparence
                    opacity = 0.3
                    fill_opacity = 0.1
                    radius = 3
                    color = "black"
            else: # On met toutes les station en noir si rien n'est précisé
                opacity = 1
                fill_opacity = 1
                radius = 4
                color = "black"

            # Ajout d'un marqueur rouge spéciale pour chaque station terminus 
            if station.terminus == 1:
                fo.Marker(location=[station.coord['lat'], station.coord['long']],
                          icon=fo.Icon(color="red", icon='train-subway', prefix="fa"),
                          opacity=opacity,
                          tooltip=f"ID: {station.id}<br><h3 style='width:100%'>{station.nom}</h3>\
                        <table style='width:100% ; border: 1px solid;' >\
                            <tr{bordure_css}><th {bordure_css}> Ligne</th><th {bordure_css}>Terminus</th> <th {bordure_css}>Latitude</th><th {bordure_css}> Longitude</th>\
                            <tr {bordure_css}><td {bordure_css}>{station.ligne}</td> <td {bordure_css}>{station.terminus}</td><td {bordure_css}>{station.coord['lat']}</td><td {bordure_css}>{station.coord['long']}</d></tr>\
                        </table>").add_to(self.layer_ligne[station.ligne])
                
            # Ajout d'un marqueur pour chaque station avec ses coordonnées et une icône de métro
            elif station.terminus == 0:
                fo.CircleMarker(location=[station.coord['lat'], station.coord['long']],
                                opacity=opacity,
                                radius=radius,
                                color=color,
                                fill=True,
                                fill_opacity=fill_opacity,
                                tooltip=f"ID: {station.id}<br><h3 style='width:100%'>{station.nom}</h3>\
                        <table style='width:100% ; border: 1px solid;' >\
                            <tr{bordure_css}><th {bordure_css}> Ligne</th><th {bordure_css}>Terminus</th> <th {bordure_css}>Latitude</th><th {bordure_css}> Longitude</th>\
                            <tr {bordure_css}><td {bordure_css}>{station.ligne}</td> <td {bordure_css}>{station.terminus}</td><td {bordure_css}>{station.coord['lat']}</td><td {bordure_css}>{station.coord['long']}</d></tr>\
                        </table>").add_to(self.layer_ligne[station.ligne])
        return self.zone_map.save('static/map.html')
    
    # Fonction qui trace les lignes de métro sur la map
    def draw_metro_line(self, metro_obj, lst_ligne=None):
        # Pour chaque ligne de metro
        for line in range(len(self.liste_ligne)):
            color = self.color_line[self.liste_ligne[line]]
            # On stock chaque station situé sur la ligne
            lst_station_object = [i for i in metro.get_stations_obj_of_line(metro_obj, self.liste_ligne[line])]
            # On part d'une station source
            for source in range(len(lst_station_object)):
                lst_source_relation = [target[0] for target in metro_obj.graph._edges[
                    lst_station_object[source].id]]  # On construit une liste de station lié à la station source
                # On regarde si les autres stations sont présent dans liste des relation en évitant les doublons.
                for target in range(source + 1, len(lst_station_object)):
                    # On trace la ligne si il y a relation
                    if lst_station_object[target].id in lst_source_relation:
                        if lst_ligne is not None:
                            if self.liste_ligne[line] in lst_ligne:  # On met en évidence les lignes sélectionnées
                                opacity = 1
                                weight = 6
                            else: # On met en transparence le reste
                                opacity = 0.4
                                weight = 2
                            fo.PolyLine(
                                [(lst_station_object[source].coord['lat'], lst_station_object[source].coord['long']),
                                 (lst_station_object[target].coord['lat'], lst_station_object[target].coord['long'])],
                                color=color, tooltip=self.liste_ligne[line], weight=weight, opacity=opacity).add_to(
                                self.layer_ligne[self.liste_ligne[line]])
                        else: 
                            fo.PolyLine(
                                [(lst_station_object[source].coord['lat'], lst_station_object[source].coord['long']),
                                 (lst_station_object[target].coord['lat'], lst_station_object[target].coord['long'])],
                                color=color, tooltip=self.liste_ligne[line], weight=4, opacity=1).add_to(
                                self.layer_ligne[self.liste_ligne[line]])

        fo.LayerControl().add_to(self.zone_map)
        return self.zone_map.save('static/map.html')

    # Fonction qui trace le plus court trajet d'une station à une autre
    def draw_bellmanford(self, metro, station1, station2 ,station_etape = None):
        bordure_css = "style='border: 1px solid;'"

        station_name=[]
        if station_etape is not None: # Si on choisis une station étapes
            bellman_ford = metro.trajet_station_tiers(station1,station_etape,station2)
        else: # Entre deux stations
            bellman_ford = metro.graph.bellman_ford(station1, station2)

        bellmanford_station_obj = []
        # On échange les stations id avec leurs objets dans une liste 
        for station_id in bellman_ford[0]:
            for station_obj in metro.station:
                if station_id == station_obj.id:
                    bellmanford_station_obj.append(station_obj)
                    station_name.append(station_obj.nom)

        # On recrée la map avec un zoom sur la station départ
        self.zone_map = fo.Map(location=[bellmanford_station_obj[0].coord['lat'], bellmanford_station_obj[0].coord['long']], zoom_start=14)
        for line, layer in self.layer_ligne.items():
            self.zone_map.add_child(layer)
        self.zone_map.get_root().html.add_child(fo.Element(self.legend_html))

        # Draw line
        for i in range(len(bellmanford_station_obj) - 1):
            fo.PolyLine(
                [(bellmanford_station_obj[i].coord['lat'], bellmanford_station_obj[i].coord['long']),
                 (bellmanford_station_obj[i + 1].coord['lat'], bellmanford_station_obj[i + 1].coord['long'])],
                color=self.color_line[bellmanford_station_obj[i].ligne],
                tooltip=f"<h5 style='font-weight:bold'>TEMPS DE TRAJET TOTALE: {bellman_ford[1]} secondes</h5>\
                        <label style='font-weight:bold ; font-size:12px'>Trajet en cours:</label> {bellmanford_station_obj[i].id} {station_name[i]} --> {bellmanford_station_obj[i+1].id} {station_name[i+1]}<br>\
                        <label style='font-weight:bold ; font-size:12px'>Ligne: </label> {bellmanford_station_obj[i].ligne}",
                weight=8, opacity=1).add_to(
                self.layer_ligne[bellmanford_station_obj[i].ligne])

        # Draw marker
        for station_obj in range(len(bellmanford_station_obj)):
            # Cas ou c'est la station de départ
            if bellmanford_station_obj[station_obj].id == station1:
                fo.Marker(location=[bellmanford_station_obj[station_obj].coord['lat'],
                                    bellmanford_station_obj[station_obj].coord['long']],
                          icon=fo.Icon(color="black", icon='flag-checkered', prefix="fa"),
                          opacity=1,
                          tooltip=f"ID: {bellmanford_station_obj[station_obj].id}<br><h3 style='width:100%'>{bellmanford_station_obj[station_obj].nom}</h3>\
                                                        <table style='width:100% ; border: 1px solid;' >\
                                                            <tr{bordure_css}><th {bordure_css}> Ligne</th><th {bordure_css}>Terminus</th> <th {bordure_css}>Latitude</th><th {bordure_css}> Longitude</th>\
                                                            <tr {bordure_css}><td {bordure_css}>{bellmanford_station_obj[station_obj].ligne}</td> <td {bordure_css}>{bellmanford_station_obj[station_obj].terminus}</td><td {bordure_css}>{bellmanford_station_obj[station_obj].coord['lat']}</td><td {bordure_css}>{bellmanford_station_obj[station_obj].coord['long']}</d></tr>\
                                                        </table>").add_to(
                    self.layer_ligne[bellmanford_station_obj[station_obj].ligne])
            # Cas ou c'est la station de destination
            elif bellmanford_station_obj[station_obj].id == station2:
                fo.Marker(location=[bellmanford_station_obj[station_obj].coord['lat'],
                                    bellmanford_station_obj[station_obj].coord['long']],
                          icon=fo.Icon(color="red", icon='circle', prefix="fa"),
                          opacity=1,
                          tooltip=f"ID: {bellmanford_station_obj[station_obj].id}<br><h3 style='width:100%'>{bellmanford_station_obj[station_obj].nom}</h3>\
                                                        <table style='width:100% ; border: 1px solid;' >\
                                                            <tr{bordure_css}><th {bordure_css}> Ligne</th><th {bordure_css}>Terminus</th> <th {bordure_css}>Latitude</th><th {bordure_css}> Longitude</th>\
                                                            <tr {bordure_css}><td {bordure_css}>{bellmanford_station_obj[station_obj].ligne}</td> <td {bordure_css}>{bellmanford_station_obj[station_obj].terminus}</td><td {bordure_css}>{bellmanford_station_obj[station_obj].coord['lat']}</td><td {bordure_css}>{bellmanford_station_obj[station_obj].coord['long']}</d></tr>\
                                                        </table>").add_to(
                    self.layer_ligne[bellmanford_station_obj[station_obj].ligne])
            else:  # Autre station
                # Pas de correspondance
                if bellmanford_station_obj[station_obj].ligne == bellmanford_station_obj[station_obj - 1].ligne and \
                        bellmanford_station_obj[station_obj].ligne == bellmanford_station_obj[station_obj + 1].ligne:
                    color = "black"
                    radius = 4
                # Correspondance
                else:
                    color = "white"
                    radius = 6
                # Ajout d'un marqueur pour chaque station avec ses coordonnées et une icône de métro
                fo.CircleMarker(location=[bellmanford_station_obj[station_obj].coord['lat'],
                                          bellmanford_station_obj[station_obj].coord['long']],
                                opacity=1, radius=radius, color=color, fill=True, fill_opacity=1,
                                tooltip=f"ID: {bellmanford_station_obj[station_obj].id}<br><h3 style='width:100%'>{bellmanford_station_obj[station_obj].nom}</h3>\
                                                    <table style='width:100% ; border: 1px solid;' >\
                                                        <tr{bordure_css}><th {bordure_css}> Ligne</th><th {bordure_css}>Terminus</th> <th {bordure_css}>Latitude</th><th {bordure_css}> Longitude</th>\
                                                        <tr {bordure_css}><td {bordure_css}>{bellmanford_station_obj[station_obj].ligne}</td> <td {bordure_css}>{bellmanford_station_obj[station_obj].terminus}</td><td {bordure_css}>{bellmanford_station_obj[station_obj].coord['lat']}</td><td {bordure_css}>{bellmanford_station_obj[station_obj].coord['long']}</d></tr>\
                                                    </table>").add_to(
                    self.layer_ligne[bellmanford_station_obj[station_obj].ligne])

        fo.LayerControl().add_to(self.zone_map)
        return self.zone_map.save('static/map.html')

    # Fonction qui trace les stations adjacente d'une station saisie
    def drawn_station_proche(self, metro , station):
        lst_station = metro.stations_proches(station)
        lst_station.append(station)
        lst_station_obj = []
        station_name=[]

        bordure_css = "style='border: 1px solid;'"
        # On fait correspondre les station id avec la station objet
        for station_id in lst_station:
            for station_obj in metro.station:
                if station_id == station_obj.id:
                    lst_station_obj.append(station_obj)
                    station_name.append(station_obj.nom)

        # On recrée la map avec un zoom sur la station départ
        self.zone_map = fo.Map(
            location=[lst_station_obj[-1].coord['lat'], lst_station_obj[-1].coord['long']], zoom_start=14)
        for line, layer in self.layer_ligne.items():
            self.zone_map.add_child(layer)
        self.zone_map.get_root().html.add_child(fo.Element(self.legend_html))


        # Draw line
        for i in range(len(lst_station_obj) - 1):
            fo.PolyLine(
                [(lst_station_obj[-1].coord['lat'], lst_station_obj[-1].coord['long']),
                 (lst_station_obj[i].coord['lat'], lst_station_obj[i].coord['long'])],
                color=self.color_line[lst_station_obj[i].ligne],
                tooltip=f"<h5 style='font-weight:bold;text-align:center'>ADJACENCE: ID {station} -- ID {lst_station_obj[i].id}</h5>",
                weight=8, opacity=1).add_to(
                self.layer_ligne[lst_station_obj[i].ligne])

        for station_obj in range(len(lst_station_obj)):
            if lst_station_obj[station_obj].id == station:# Cas ou c'est la station de départ
                fo.Marker(location=[lst_station_obj[station_obj].coord['lat'],
                                    lst_station_obj[station_obj].coord['long']],
                          icon=fo.Icon(color="black", icon='flag-checkered', prefix="fa"),
                          opacity=1,
                          tooltip=f"ID: {lst_station_obj[station_obj].id}<br><h3 style='width:100%'>{lst_station_obj[station_obj].nom}</h3>\
                                                        <table style='width:100% ; border: 1px solid;' >\
                                                            <tr{bordure_css}><th {bordure_css}> Ligne</th><th {bordure_css}>Terminus</th> <th {bordure_css}>Latitude</th><th {bordure_css}> Longitude</th>\
                                                            <tr {bordure_css}><td {bordure_css}>{lst_station_obj[station_obj].ligne}</td> <td {bordure_css}>{lst_station_obj[station_obj].terminus}</td><td {bordure_css}>{lst_station_obj[station_obj].coord['lat']}</td><td {bordure_css}>{lst_station_obj[station_obj].coord['long']}</d></tr>\
                                                        </table>").add_to(
                self.layer_ligne[lst_station_obj[station_obj].ligne])

            else: # Cas ou c'est la station de destination
                fo.Marker(location=[lst_station_obj[station_obj].coord['lat'],
                                    lst_station_obj[station_obj].coord['long']],
                          icon=fo.Icon(color="red", icon='circle', prefix="fa"),
                          opacity=1,
                          tooltip=f"ID: {lst_station_obj[station_obj].id}<br><h3 style='width:100%'>{lst_station_obj[station_obj].nom}</h3>\
                                                        <table style='width:100% ; border: 1px solid;' >\
                                                            <tr{bordure_css}><th {bordure_css}> Ligne</th><th {bordure_css}>Terminus</th> <th {bordure_css}>Latitude</th><th {bordure_css}> Longitude</th>\
                                                            <tr {bordure_css}><td {bordure_css}>{lst_station_obj[station_obj].ligne}</td> <td {bordure_css}>{lst_station_obj[station_obj].terminus}</td><td {bordure_css}>{lst_station_obj[station_obj].coord['lat']}</td><td {bordure_css}>{lst_station_obj[station_obj].coord['long']}</d></tr>\
                                                        </table>").add_to(
                    self.layer_ligne[lst_station_obj[station_obj].ligne])

        fo.LayerControl().add_to(self.zone_map)
        return self.zone_map.save('static/map.html')


    # Fonction qui trace l'arbre couvrant minimale
    def draw_acm(self, metro):
        acm = metro.acm() 
        bordure_css = "style='border: 1px solid;'"

        # On fait correspondre les stations dans les relations avec leurs objets
        for relation in acm:
            station1_id = relation.id1
            station2_id = relation.id2
            for station_obj in metro.station:
                if station_obj.id == station1_id:
                    station1 = station_obj
                elif station_obj.id == station2_id:
                    station2 = station_obj
            if station1.id == 0: # Dans le cas où c'est la stations de départ
                color = "red"
                radius = 8
            # On trace une ligne de la station antécédente vers sa prochaine dans la liste
            fo.PolyLine(
                [(station1.coord['lat'], station1.coord['long']),
                 (station2.coord['lat'], station2.coord['long'])],
                color=self.color_line[station2.ligne],
                tooltip=f"<h5 style='font-weight:bold'>{station1.id} {station1.nom} --> {station2.id} {station2.nom}</h5>\
                                    <label style='font-weight:bold'>Ligne: </label> {station2.ligne}",
                weight=8, opacity=1).add_to(self.layer_ligne[station2.ligne])

            # On place son marqueur
            fo.CircleMarker(location=[station1.coord['lat'],station1.coord['long']],
                            opacity=1, radius=radius, color=color, fill=True, fill_opacity=1,
                            tooltip=f"ID: {station1.id}<br><h3 style='width:100%'>{station1.nom}</h3>\
                                    <table style='width:100% ; border: 1px solid;' >\
                                        <tr{bordure_css}><th {bordure_css}> Ligne</th><th {bordure_css}>Terminus</th> <th {bordure_css}>Latitude</th><th {bordure_css}> Longitude</th>\
                                        <tr {bordure_css}><td {bordure_css}>{station1.ligne}</td> <td {bordure_css}>{station1.terminus}</td><td {bordure_css}>{station1.coord['lat']}</td><td {bordure_css}>{station1.coord['long']}</d></tr>\
                                    </table>").add_to(self.layer_ligne[station1.ligne])
            
           
            if station2.terminus == 1: # Dans le cas où la station prochaine est terminus (marque aussi les derniers noeud de l'arbre)
                color = "blue"
                radius = 5
            else: # Sinon marqueur normale
                color = "black" 
                radius= 4

            # On place la station prochaine 
            fo.CircleMarker(location=[station2.coord['lat'],station2.coord['long']],
                            opacity=1, radius=radius, color=color, fill=True, fill_opacity=1,
                            tooltip=f"ID: {station2.id}<br><h3 style='width:100%'>{station2.nom}</h3>\
                                    <table style='width:100% ; border: 1px solid;' >\
                                        <tr{bordure_css}><th {bordure_css}> Ligne</th><th {bordure_css}>Terminus</th> <th {bordure_css}>Latitude</th><th {bordure_css}> Longitude</th>\
                                        <tr {bordure_css}><td {bordure_css}>{station2.ligne}</td> <td {bordure_css}>{station2.terminus}</td><td {bordure_css}>{station2.coord['lat']}</td><td {bordure_css}>{station2.coord['long']}</d></tr>\
                                    </table>").add_to(self.layer_ligne[station2.ligne])
            color = "black"
            radius = 4

        fo.LayerControl().add_to(self.zone_map)
        return self.zone_map.save('static/map.html')
