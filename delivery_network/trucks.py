from graph import Graph, graph_from_file

global budget
global g

budget = 25000000000
g = graph_from_file("/home/onyxia/ProjetProg-Ensae-1/delivery_network/input/network.1.in")

def store(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        lines.pop(0)
        store = []
        for line in lines:
            store += [line.split()]
    return list(map(lambda x: [int(k) for k in x], store))


def clean_store(store):
    maxPrice = store[-1][1] + 1
    clean_store = []
    for k in range(len(store)-1, -1, -1):
        if store[k][1] < maxPrice:
            clean_store.append(store[k])
            maxPrice = store[k][1]
    clean_store.reverse()
    return clean_store


def routes(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        lines.pop(0)
        routes = []
        for line in lines:
            line = line.split()
            line = list(map(int, line))
            routes += [line + [g.min_power_kruskal(line[0], line[1])[1]]]
    return routes


def buylist(store, routes):
    
    return

def Collection_de_camions(filename1, filename2, budget):

    camions=clean_store(store(filename1))
    routes=Routes(filename2)
    Dico=dict([(n, []) for n in range(len(routes))])
    for n in range(len(routes)):
        Dico[n]=routes[n]

    # Etape 1: Création d'un dictionnaire associant chaque route au camion le moins cher pouvant la traverser
    d=dict([(n, []) for n in range(len(routes))])
    A=[]
    for camion in camions:
        A.append(camion[0])
    M=max(A)
    for i in range(len(routes)):
        route=routes[i]
        power_min=M
        for camion in camions:
            if camion[0]<power_min and camion[0]>=route[3]:
                power_min=camion[0]
        d[i]=power_min

    # Etape 2: On fait une liste de listes de routes pour lesquelles on ne dépasse pas le budget
    listes_routes=[]
    for i in range(len(d)):
        pathsi=[[d[i]]]
        b=budget-d[i][1]
        while b>0:
            path=pathsi.pop(0)
            for j in d:
                if B[path][i]-d[j][1]>0 and j not in path:
                    path.append(j)
            pathsi.append(path)
            B=dict([(path, budget) for path in pathsi])
            for path in pathsi:
                b=0
                for route in path:
                    B[path]= B[path]-d[route][1]
                if B[path]>b:
                    b=B[path]
        for path in pathsi:
            listes_routes.append(path)
    
    #Etape 3: On sélectionne la liste de routes avec le plus grand profit
    P=[0 for i in range(listes_routes)]
    for i in len(listes_routes):
        for route in listes_routes[i]:
            P[i]=route[2]
    profit=max(P)
    j=listes_routes.index(profit)
    return(listes_routes(j))


print(routes("/home/onyxia/ProjetProg-Ensae-1/delivery_network/input/routes.1.in"))











































