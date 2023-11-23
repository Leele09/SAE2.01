from flask import Flask, render_template, request, jsonify , redirect

import pandas as pd
from Graph import Graph
from metro import *
from relation import *
from station import *
from Carte import *
import json
import numpy as np

app = Flask(__name__)


@app.route('/')
def index():

    # CONSTRUCTION DE LA MAP DE BASE
    map = Map(metro.station , [ligne for ligne in set(stations["ligne"])])
    map.draw_metro_line(metro,[ligne for ligne in set(stations["ligne"])])
    map.draw_marker(metro,[ligne for ligne in set(stations["ligne"])])

    return render_template('index.html')

# Route qui gère le filtrage de la map et les lignes à afficher
@app.route('/filtrage' ,methods=["GET","POST"])
def filtrage_ligne():
    # On récupère le contenu du paquet
    selected_line = request.form.get('lst_Ligne_coche')
    selected_line = json.loads(selected_line)

    # On recrée la map avec les lignes voulus
    map = Map(metro.station, [ligne for ligne in set(stations["ligne"])])
    map.draw_metro_line(metro, selected_line)
    map.draw_marker(metro , selected_line)
    return jsonify(map_a_jour = True)


# Fonction qui gère les algorithmes selectionnée
@app.route('/algo_comparaison' ,methods=["GET","POST"])
def algo_comparaison():
    selected_algo = request.form["algo"]  # On récupère l'algo selectionné

    # Si rien n'est selectionné rien ne se passe
    if selected_algo == "0":
        return redirect('/')
    
    elif selected_algo == "1":  # Chemin possible
        source = int(request.form['station1'])
        destination = int(request.form['station2'])
        # On trouve les trajets possible
        reponse = metro.trajet_possible(source,destination)
        return jsonify(trajet=reponse)
    
    elif selected_algo == "2":  # Bellman Ford
        source = int(request.form['station1'])
        destination = int(request.form['station2'])
        # Pas de station intermédiaire spécifiée
        if request.form['station_etape'] == "":
            map = Map(metro.station, [ligne for ligne in set(stations["ligne"])])
            map.draw_bellmanford(metro, source, destination)
        # Avec une station intermédiaires
        else:
            station_etape = int(request.form['station_etape'])
            map = Map(metro.station, [ligne for ligne in set(stations["ligne"])])
            map.draw_bellmanford(metro, source, destination,station_etape)
        return jsonify(map_a_jour=True )
    
    elif selected_algo == "3": # Analyse accessibilité
        source = int(request.form['station1'])
        destination = int(request.form['station2'])
        distance = int(request.form['distance'])

        # On trouve les accessibilité entre les deux station en fonction d'une distance donnée 
        reponse = metro.plus_accessible(source, destination, distance)
        acc = reponse[0] # accessible
        cen = reponse[1] # centrale
        term = reponse[2] # terminale
        return jsonify(acc = acc , cen = cen, term = term)  

    elif selected_algo == "4": # Arbre couvrant minimale
        # On trace l'arbre couvrant
        map = Map(metro.station, [ligne for ligne in set(stations["ligne"])])
        map.draw_acm(metro)
        return jsonify(map_a_jour=True )

    elif selected_algo == "5": # Analyse p-distance
        source = int(request.form['station1'])
        destination = int(request.form['station2'])
        distance = int(request.form['distance'])
        reponse = metro.reliees_p_distance(source, destination, distance)
        return jsonify(p_distance = reponse[0]  , chemin = reponse[1] , color = reponse[2])

    elif selected_algo == "6": # Station proche
        source = int(request.form['station1'])
        reponse = metro.stations_proches(source)
        # On recrée la map avec le traçage des tations proche de la source
        map = Map(metro.station, [ligne for ligne in set(stations["ligne"])])
        map.drawn_station_proche(metro, source)
        print(reponse)
        return jsonify(map_a_jour=True )
    return redirect('/')

# Procédure qui démarre le server Flask
def run_server():
    print("Lancement du server Flask")
    app.run(debug=True)


if __name__ == '__main__':
    # LECTURE DES CSV
    relations = pd.DataFrame(pd.read_csv("Données/relations.csv", sep=";"))
    stations = pd.DataFrame(pd.read_csv("Données/stations.csv", sep=";"))
    coord = pd.DataFrame(pd.read_csv("Données/coord_geo.csv", sep=";"))
    station_coord = pd.concat([stations,coord[['latitude','longitude']]],axis=1)

    # CREATION DU RESEAU
    metro = metro() 

    # INSERTION DES STATIONS ET DES RELATIONS DANS LE RESEAU - CONSTRUCTION DU GRAPH
    for lines in station_coord.values:
        metro.add_station(station(lines[0], lines[1] , lines[2] , lines[3].replace("_"," ") ,lines[4],lines[5]))
    for lines in relations.values:
        metro.add_relation(Relation(lines[0], lines[1], lines[2]))
    metro.construire_graph()

    # LANCEMENT DU SERVER FLASK
    run_server()

