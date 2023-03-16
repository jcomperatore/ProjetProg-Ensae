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


print(routes("/home/onyxia/ProjetProg-Ensae-1/delivery_network/input/routes.1.in"))











































