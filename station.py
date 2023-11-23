class station:
    def __init__(self , id , ligne , terminus , nom ,latitude,longitude):
        self.id = id  # Identifiant de la station
        self.ligne = ligne  # Ligne du métro à laquelle la station appartient
        self.terminus = terminus  # Indicateur si la station est un terminus
        self.nom = nom  # Nom de la station
        self.coord = {}  # Dictionnaire pour stocker les coordonnées de la station
        self.coord['lat'] = latitude  # Latitude de la station
        self.coord['long'] = longitude  # Longitude de la station

    def __str__(self):
        return f'id {self.id} | line {self.ligne} | terminus {self.terminus} | name {self.nom} | coordinates {self.coord}'
