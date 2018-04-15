# -*- coding: utf-8 -*-
import pants
import csv
import geopy.distance
import time
import networkx as nx
import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt

nodes = []
data = []
fileName = None
tempsdebut = time.time()


def readCSV():
    global fileName
    if fileName == None:
        fileName = input("Entrer le nom du fichier :")  # 1 ou 2 ou 3 ou 4 ou 5
    if(fileName is not  None):
        with open('files/test' + fileName + '.csv', 'r') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(csvReader)
            for row in csvReader:
                if row:
                    latitude = row[6]
                    longitude = row[7]

                    print("latitude : " + latitude, "longitude : " + longitude)
                    try:
                        if (latitude !='' and  longitude != '' and
                                latitude != '/N' and longitude != '/N' and
                                isinstance(float(latitude), float) and isinstance(float(longitude), float)):
                            nodes.append((float(latitude), float(longitude)))
                    except Exception as ex:  # latitude contient "/N" ou longitude contient "/N"
                        print(format(ex))

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # Si la valeur n'a pas encore été rencontrée,
        # ... ... ajoutez-le à la liste et à l'ensemble
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

def CalculDistance(coords_a, coords_b):
    dist = geopy.distance.vincenty(coords_a, coords_b).km
    # TEST
    # print("dist: " + format(dist)  + '/n')
    return dist


def createWorld():
    try:
        if(isinstance( nodes, type([]))):
            data = remove_duplicates(nodes)
            return pants.World(data, CalculDistance)
    except Exception as ex:
        print("createWorld : " + format(ex.args))


def createSolver():
    try:
        return pants.Solver()
    except Exception as ex:
        print("createSolver : " + format(ex))



def methodeSolve(solver, world):
    try:
        if solver is None or world is None:
            print("solver ou world None")
        else:
            solution = solver.solve(world)  # renvoie la meilleure solution trouvée
            if solution is None:
                print("solution None")
            # Afficher la Meilleur distance trouvée par solve
            else:
                print("")
                print("--------------------------------------------------------------------------------")
                print("Meilleur Distance trouvée par solver.solve(world) : " + format(solution.distance) + " KM")
                print("--------------------------------------------------------------------------------")
                print("Noeuds visités : " + format(solution.tour))  # noeuds visités
                print("--------------------------------------------------------------------------------")
                print("Edges  prises : " + format(solution.path))  # Edges  prises
                print("--------------------------------------------------------------------------------")
                neoudsVisiter = solution.tour
                return neoudsVisiter
    except Exception as ex:
        print("error in methodeSolve : " + format(ex))


def methodeSolutions(solver, world):
    try:
        # renvoie chaque solution trouvée si elle est la meilleure jusqu'à présent
        solutions = solver.solutions(world)
        if solutions is None:
            print("solutions None")
        else:
            i = 1
            bestSolution = float("inf")
            for sol in solutions:
                # Afficher les solutions optimaux
                print("")
                print("Distance " + format(i) + " : " + format(sol.distance) + " KM")
                i += 1
                assert sol.distance < bestSolution
                bestSolution = sol.distance

                # Afficher la Meilleur distance
            print("")
            print("--------------------------------------------------------------------------------")
            print("Meilleur Distance trouvée par solver.solutions(world) : " + format(bestSolution) + " KM")
            print("--------------------------------------------------------------------------------")
            print("")
    except Exception as ex:
        print("error in methodesolutions : " + format(ex))

def calculerTempsExecution():
    try:
        # temps fin d'exécution
        tempsfin = time.time()
        # Calculer le temps d'exécution
        TempsEx = tempsfin - tempsdebut
        # Afficher le temps d'exécution
        print("")
        print("--------------------------------------------------------------------------------")
        print("Temps d'exécution : " + format(TempsEx) + " secondes")
        print("--------------------------------------------------------------------------------")
        print("")
    except Exception as ex:
        print("calculerTempsExecution : " + format(ex))


def printSolution(solver, world):
    try:
        if(type(solver) and type(world)):
            # renvoie chaque solution trouvée si elle est la meilleure jusqu'à présent
            methodeSolutions(solver, world)
            # renvoie la meilleure solution trouvée
            neoudsVisiter = methodeSolve(solver, world)
            # calculer le temps d'exécution
            calculerTempsExecution()
            # affichage du graphe
            createGraph(neoudsVisiter)
    except Exception as ex:
        print("printSolution : " + format(ex))



def createGraph(neoudsVisiter):
    G = nx.Graph()
    # G.add_edges_from(neoudsVisiter)
    for neoud in neoudsVisiter:
        G.add_edge(format(neoud[0]), format(neoud[1]), weight=0.6)
    plt.subplot(121)

    node_positions = nx.spring_layout(G)  # positions for all nodes
    nx.draw_networkx(G, pos=node_positions, node_size=100, node_color='red', edge_color="green", with_labels=True,
                     alpha=1)

    edge_labels = nx.get_edge_attributes(G, 'sequence')
    nx.draw_networkx_edge_labels(G, pos=node_positions, edge_labels=edge_labels, font_size=20)
    nx.draw_networkx_nodes(G, pos=node_positions, node_size=20)
    nx.draw_networkx_edges(G, pos=node_positions, alpha=0.4)

    plt.xticks([])
    plt.yticks([])

    plt.text(0.5, 0.5, G, ha="center", va="center", size=24, alpha=.5)
    plt.title('Noeuds Visitées', size=15)

    plt.ylabel("Y")
    plt.xlabel("X")
    plt.axis('off')

    plt.subplot(122)
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    print("Degree sequence", degree_sequence)
    dmax = max(degree_sequence)
    plt.loglog(degree_sequence, 'b-', marker='o')
    plt.title("Courbe")
    plt.ylabel("Degree")
    plt.xlabel("Rank")

    # dessine le graphique dans l'encart
    plt.axes([0.45, 0.45, 0.45, 0.45])
    Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
    pos = nx.spring_layout(Gcc)
    plt.axis('off')
    nx.draw_networkx_nodes(Gcc, pos, node_size=20)
    nx.draw_networkx_edges(Gcc, pos, alpha=0.4)
    plt.xticks([])
    plt.yticks([])
    plt.text(0.5, 0.5, Gcc, ha="center", va="center", size=24, alpha=.5)
    plt.show()


def main():
    try:
        readCSV()
        world = createWorld()
        solver = createSolver()
        printSolution(solver, world)
    except Exception as ex:
        print("main : " + format(ex))



main()