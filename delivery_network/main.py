from graph import Graph, graph_from_file


data_path = "/home/onyxia/ProjetProg-Ensae/delivery_network/input/"
data_path = "/Users/julescomperatore/ProjetProg-Ensae/delivery_network/input/"
file_name = "network.2.in"

g = graph_from_file(data_path + file_name)
#print(g.connected_components())

kruskal = g.kruskal()
#print(kruskal)
print(g.kruskal())
print(g.get_path_with_kruskal(1, 20, g.kruskal_path(kruskal)))
print(g.min_power_kruskal(1, 20, kruskal))





