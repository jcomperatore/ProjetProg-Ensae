class Graph:
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
    

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        
        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        
        self.nb_edges += 1
        
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is
         added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        return
    

    def mini(listeSommets, marque):
        """
        Renvoie le sommet de listeSommets
        ayant la plus petite marque.
        """
        marquePlusPetite = inf
        for s in listeSommets:
            if marque[s] < marquePlusPetite:
                marquePlusPetite = marque[s]
                sommetPlusPetit = s
        return sommetPlusPetit

    def dijkstra(graphe, depart, arrivee):

        # initialisation
        marque = {}
        for sommet in graphe: marque[sommet] = inf
        marque[depart] = 0

        non_selectionnes = [sommet for sommet in graphe]

        pere = {}
        pere[depart] = None

        # boucle principale:
        while non_selectionnes:
            # sélection:
            s = mini(non_selectionnes, marque)
            if s == arrivee: break
            non_selectionnes.remove(s)

            # mise à jour des voisins du sommet sélectionné:
            VoisinsAVisiter = [sommet for sommet in graphe[s] if sommet in non_selectionnes]
            for sommet in VoisinsAVisiter:
                p = marque[s] + graphe[s][sommet]
                if p < marque[sommet]:
                    marque[sommet] = p
                    pere[sommet] = s

        return marque, pere    
    
    def get_path_with_power(self, src, dest, power):
        
 
 
 
 
 
 
 
 
 
   """     if power <= 0 : return None

        cc = self.connected_components_set()  
        impossible = True
        for k in cc : 
            if src in k and dest in k : 
                impossible = False
                cc=k
                break

        if impossible : 
            return None

        visited = set()
        path = []
        
        def pathExplore(step, remainingPower):
            visited.add(step)
            print(visited)
            print(path)
            for node in self.graph[step] :
                if node[0] == dest :
                    if node[2] <= remainingPower :
                        path.append(node[0])
                        return path

                elif node[0] not in visited:
                    if node[2] <= remainingPower :
                        path += [node[0]]
                        path.extend(pathExplore(node[0], remainingPower - node[2]))
                    else : visited.add(node[0])
                    
            if path[-1] == dest : return path
            return None

        return pathExplore(src, power)
"""

    

    def connected_components(self):
        
        visited = set()  # On crée une variable contenant l'ensemble des noeuds qui ont déjà été étudié par la méthode
        components = []  # On crée la liste des composantes connexes, que l'on initialise comme vide

        def nodeComponent(node):  # On crée une fonction qui nous permettra de relier le noeud à tous les autres noeuds de sa composante connexe
            visited.add(node)     # Le noeud étudié est rajouté à la liste des noeuds étudiés
            component = [node]    # Variable locale qui nous permettra de créer la composante
            for neighbor in self.graph[node]:  # On parcourt déjà les voisins directs du noued étudié
                if neighbor[0] not in visited:  # Pas besoin de réétudier les noeuds déjà traités. Permet à la boucle récursive de bien terminer
                    component.extend(nodeComponent(neighbor[0]))  # On ajoute récursivement les composantes connexes des voisins directs du noeud
            return component 

        for node in self.graph:  # On parcourt tous les noeuds du graphe
            if node not in visited:  # Pas besoin de réétudier les noeuds déjà traités.
                components.append(nodeComponent(node))  # On rajoute à la liste des composantes chacune des composante

        return components  #Renvoie une liste de liste de la forme [[Composante connexe 1],[autre composante connexe], ... ]


    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    
    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        raise NotImplementedError


def graph_from_file(filename):
    file = open(filename, 'r')
    nodes = []
    lines = file.readlines() 
    line1 = lines.pop(0).split()
    nodes = range(1, int(line1[0]) + 1)
    
    graph = Graph(nodes)
    for line in lines :    
        data = [int(x) for x in line.split()]    
        if len(data) == 3 :
             graph.add_edge(data[0], data[1], data[2])
        else :
             graph.add_edge(data[0], data[1], data[2], data[3])




    file.close()
    
    
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    G: Graph
        An object of the class Graph with the graph from file_name.
    """
    return graph
