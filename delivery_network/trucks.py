from graph import Graph, graph_from_file

data_path = "/home/onyxia/ProjetProg-Ensae/delivery_network/input/"
data_path = "C:/Users/jules/Desktop/ProjetProg-Ensae/ProjetProg-Ensae/delivery_network/input/"
file_number = 2
file_name = "network."+ str(file_number) +".in"
route_name = "routes."+ str(file_number) +".in"
trucks_name = "trucks."+ str(2) +".in"

global g

budget = 25000000000
g = graph_from_file(data_path + file_name)

kruskal = g.kruskal()
ancetres = g.kruskal_path()
#ccs = g.connected_components_set()


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


def lire_routes(filename, kruskal, ancetres):
    with open(filename, "r") as file:
        lines = file.readlines()
        lines.pop(0)
        routes = []
        for line in lines:
            line = line.split()
            line = list(map(int, line))
            routes += [line + [g.min_power_kruskal(line[0], line[1], kruskal, ancetres)[1]]]
    return routes


def buylist(store, routes):
    
    return

def Collection_de_camions_naïf(filename1, filename2, budget):

    camions=clean_store(store(filename1))
    routes=lire_routes(filename2,kruskal,ancetres,ccs)
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
    for i in d:
        N=0
        paths1=[[i]]
        b=budget-d[i]
        B=[b for n in range(len(paths1))]
        while b>0:
            path=paths1.pop(0)
            for j in d:
                if B[0]-d[j]>0 and j not in path:
                    path.append(j)
                paths1.append(path)
                N+=1
            if N==(len(routes)-1)**(len(routes)-1):
                break
            B=[b for n in range(len(paths1))]
            for j in range(len(paths1)):
                b=0
                path=paths1[j]
                for route in path:
                    B[j]=B[j]-d[route]
                if B[j]>b:
                    b=B[j]
        for path in paths1:
            listes_routes.append(path)
    
    #Etape 3: On sélectionne la liste de routes avec le plus grand profit
    P=[0 for i in range(listes_routes)]
    for i in range(len(listes_routes)):        
        for route in listes_routes[i]:
            route=Dico[route]
            P[i]=route[2]
    profit=max(P)
    j=P.index(profit)
    return(listes_routes[j])

def Collection_de_camions_greedy(filename1, filename2, budget, kruskal, ancetres):

    camions=clean_store(store(filename1))
    routes=lire_routes(filename2,kruskal,ancetres)

    # Création d'un dictionnaire associant chaque route au camion le moins cher pouvant la traverser
    d=dict([(n, []) for n in range(len(routes))])
    A=[]
    for camion in camions:
        A.append(camion[0])
    M=max(A)
    for i in range(len(routes)):
        route=routes[i]
        power_min=M
        c=[]
        for camion in camions:
            if camion[0]<power_min and camion[0]>=route[3]:
                power_min=camion[0]
                c=camion
        d[i]=c

    # Tri des routes selon le ratio profi/coût
    liste_routes=[]
    for route in range(len(routes)):
        profit=routes[route][2]
        cost=d[route][1]
        liste_routes.append([route,profit/cost])
    takeTwo = lambda elem: elem[1]
    liste_routes.sort(key=takeTwo, reverse=False) #j'ai modifié le reverse = True pour juste pouvoir pop a chaque fois
 
    # Construction de la liste de routes finale
    b=budget
    buylist=dict([(k[0], 0) for k in camions])
    affectations = dict([(k[0], []) for k in camions])
    
    """
    for i in range(len(liste_routes)):
        route, ratio = liste_routes[i]
        if d[route][1] <= b:
            b -= d[route][1]
            L.append([route])
     """
    route = liste_routes.pop()[0]
    route_info = routes[route]
    id_truck, cost = d[route]
    
    cpt, cpt_max = 0, len(liste_routes)
    while b >= 0 and cpt < cpt_max:
        buylist[id_truck] += 1
        affectations[id_truck].append([route_info[0], route_info[1]])
        
        route = liste_routes.pop()[0]
        route_info = routes[route]
        id_truck, cost = d[route]
        b -= cost
        cpt += 1

    return buylist, affectations

#print(routes(data_path + route_name, kruskal, ancetres))
print("SIUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")

print(Collection_de_camions_greedy(data_path + trucks_name, data_path + route_name, budget, kruskal, ancetres)[1])









































