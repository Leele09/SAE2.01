class Relation:
    def __init__(self, id1, id2, temps):
        self.id1 = id1  # Identifiant de la première station
        self.id2 = id2  # Identifiant de la deuxième station
        self.temps = temps  # Temps de trajet entre les deux stations

    def __str__(self):
        return f'| id {self.id1} <-> id {+self.id2} | t = {self.temps}'
    