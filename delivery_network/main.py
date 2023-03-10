from graph import Graph, graph_from_file


data_path = "/home/onyxia/ProjetProg-Ensae/delivery_network/input/"
file_name = "network.02.in"

g = graph_from_file(data_path + file_name)
#print(g)
#print(g.connected_components())

print(g.get_path_with_power(1, 2, 5))







