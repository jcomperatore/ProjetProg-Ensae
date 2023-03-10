from graph import Graph, graph_from_file


data_path = "/home/onyxia/ProjetProg-Ensae/delivery_network/input/"
file_name = "network.00.in"

g = graph_from_file(data_path + file_name)
print(g)
#print(g.connected_components())

print(g.kruskal())







