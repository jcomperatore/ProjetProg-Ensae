class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
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
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

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
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1

    def get_path_with_power(self, src, dest, power):
        visites=[False for i in range(self.nb_nodes)]
        trajets=[[src]]
        
        cc = self.connected_components_set()  
        impossible = True
        for k in cc : 
            if src in k and dest in k : 
                impossible = False
                cc=k
        
        if impossible : 
            return None
        
        if src == dest:
            return [dest]
        
        while trajets:
            path=trajets.pop(0)
            i=path[-1]
            if visites[i]==False:
                visites[i] = True
                for j in self.graph[i]:
                    path2 = path.copy()
                    if j[0] in cc and not visites[j[0]]:
                        if j[0]==dest and power>=j[1] :
                            path.append(dest)
                            return path
                    
                        if power>=j[1]:
                            path2.append(j[0])
                            trajets.append(path2)
        return None

    def min_power(self, src, dest) : 
        cc = self.connected_components_set()  
        impossible = True
        for k in cc : 
            if src in k and dest in k : 
                impossible = False
                cc=k
        
        if impossible : 
            return None
        
        min = 0
        max = 1
        possible = lambda power: self.get_path_with_power(src, dest, power) != None

        while not possible(max) :
            max *= 10
        
        cpt=0
        while max - min > 1 and cpt <= 50: 
            pow = int((max+min)/2)
            if possible(pow) : max = pow
            else : min = pow
            cpt+=1

        return [self.get_path_with_power(src, dest, max), max]


        

        
    def connected_components(self):
        
        visited = set()  # On cr??e une variable contenant l'ensemble des noeuds qui ont d??j?? ??t?? ??tudi?? par la m??thode
        components = []  # On cr??e la liste des composantes connexes, que l'on initialise comme vide

        def nodeComponent(node):  # On cr??e une fonction qui nous permettra de relier le noeud ?? tous les autres noeuds de sa composante connexe
            visited.add(node)     # Le noeud ??tudi?? est rajout?? ?? la liste des noeuds ??tudi??s
            component = [node]    # Variable locale qui nous permettra de cr??er la composante
            for neighbor in self.graph[node]:  # On parcourt d??j?? les voisins directs du noued ??tudi??
                if neighbor[0] not in visited:  # Pas besoin de r????tudier les noeuds d??j?? trait??s. Permet ?? la boucle r??cursive de bien terminer
                    component.extend(nodeComponent(neighbor[0]))  # On ajoute r??cursivement les composantes connexes des voisins directs du noeud
            return component 

        for node in self.graph:  # On parcourt tous les noeuds du graphe
            if node not in visited:  # Pas besoin de r????tudier les noeuds d??j?? trait??s.
                components.append(nodeComponent(node))  # On rajoute ?? la liste des composantes chacune des composante

        return components  #Renvoie une liste de liste de la forme [[Composante connexe 1],[autre composante connexe], ... ]
    

    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
        


    def find(self, parent, i):
        if parent[i]==i:
            return i
        return self.find(parent, parent[i])

    def find(self, parent, i):
            if i==parent[i]:
                return parent[i]
            return self.find(parent, parent[i])

    def union(self, parent, rank, a, b):
            aroot=self.find(parent,a)
            broot=self.find(parent,b)
            if rank[aroot]<rank[broot]:
                parent[aroot]=broot
            elif rank[broot]<rank[aroot]:
                parent[broot]=aroot
            else:
                parent[broot]=aroot
                rank[aroot]+=1
                
    def kruskal(self):
        #Ordonne la liste des arr??tes :
        edges = []
        for k in self.graph :
            for edge in self.graph[k]:
                print(edge)
                edges.append([k,edge[0],edge[1],edge[2]])
        takeThird = lambda elem: elem[2]
        edges.sort(key=takeThird)

        g_mst=[]
        parent=self.nodes
        rank=[0 for i in range(self.nb_nodes)]
        for node1 in self.nodes:
            for node in self.graph[node1] :
                if self.find(parent, node1)!= self.find(parent, node[0]):
                    g_mst.append(node1, node[0], node[1], node[2])
                    self.union(parent,rank,self.find(parent, node1) self.find(parent, node[0]))    
        return g_mst
    
    def min_power_kruskal(self, src, dest) :
        power = 100
        chemin = None
        while chemin == None : 
            chemin = self.kruskal().get_path_with_power(src, dest)
            power*=10
        power = 0
        for k in range(len(chemin)) : 
            for node in self.graph[chemin[k] - 1] : 
                if node[0] == chemin[k+1] :
                     power = max([node[1],power])
        return chemin + [power]




            


def graph_from_file(filename):
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
        g: Graph
            An object of the class Graph with the graph from file_name.
        """
        with open(filename, "r") as file:
            n, m = map(int, file.readline().split())
            g = Graph(range(1, n+1))
            for _ in range(m):
                edge = list(map(int, file.readline().split()))
                if len(edge) == 3:
                    node1, node2, power_min = edge
                    g.add_edge(node1, node2, power_min) # will add dist=1 by default
                elif len(edge) == 4:
                    node1, node2, power_min, dist = edge
                    g.add_edge(node1, node2, power_min, dist)
                else:
                    raise Exception("Format incorrect")
        return g


                






    
