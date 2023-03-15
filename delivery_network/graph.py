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
        """
        Complexité en O(nb_nodes*nb_edges)
        """
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
            path=trajets.pop(0)         #on étudie un des trajets possibles 
            i=path[-1]                     # dernier sommet atteint du trajet sélectionné
            if visites[i-1]==False:           # on vérifie si le sommet a déjà été atteint pour éviter de faire des boucles
                visites[i-1] = True
                for j in self.graph[i]:        # on étudie les voisins de i
                    path2 = path.copy()
                    if j[0] in cc and not visites[j[0]-1]:        # on vérifie que dest est connecté à j[0] et si le sommet a déjà été atteint pour éviter de faire des boucles
                        if j[0]==dest and power>=j[1] :
                            path.append(dest)
                            return path
                    
                        if power>=j[1]:
                            path2.append(j[0])
                            trajets.append(path2)               #on ajoute le trajet rallongé à la liste des trajets si toutes les conditions sont remplies 
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
        
        # Recherche dichotomique, complexité logarithmique (ie en O(log_2_(nb_nodes))) si on ne prend pas en compte la complexité des autres programmes
        
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
        
        visited = set()  # On crée une variable contenant l'ensemble des noeuds qui ont déjà été étudié par la méthode
        components = []  # On crée la liste des composantes connexes, que l'on initialise comme vide

        def nodeComponent(node):  # On crée une fonction DFS qui nous permettra de relier le noeud à tous les autres noeuds de sa composante connexe
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
        
    def find(self, parent, i):
        """
        Fonction récursive permettant de trouver le représentant de la classe d'équivalence d'un sommet d'un graphe
        """
        if i==parent[i]:           
            return parent[i]
        return self.find(parent, parent[i])

    def union(self, parent, rank, a, b):
        """
        Fonction permettant de trouver joindre deux classes d'équivalence selon le rang de leur représentant
        Ici, le sommet avec le plus grand rang devient le parent. Si les rangs sont identiques, alors le rang de la classe de a est augmenté. 
        Complexité en O(1)
        """
        aroot=self.find(parent,a)       #Représengtant de la classe de a
        broot=self.find(parent,b)       # Représentant de la classe de b
        if rank[aroot]<rank[broot]:
            parent[aroot]=broot
        elif rank[broot]<rank[aroot]:
            parent[broot]=aroot
        else:
             parent[broot]=aroot
             rank[aroot]+=1
                
    def kruskal(self):
        """
        Complexité en O(nb_nodes*log(nb_edges))
        """
  
        #On ordonne d'abord la liste des arrêtes par puissance croissante :
        edges = []
        for k in self.graph :
            for edge in self.graph[k]:
                print(edge)
                edges.append([k,edge[0],edge[1],edge[2]])
        takeThird = lambda elem: elem[2]
        edges.sort(key=takeThird)
        n=1
        k=0
        node1=1
        parent=[0]
        for node in self.nodes:
            parent.append(node)
        rank=[0 for i in range(self.nb_nodes+1)]
        g_mst=dict([(n, []) for n in self.nodes])
        while n < self.nb_nodes:
            edge = edges[k]
            k += 1
            i = self.find(parent, edge[0])
            j = self.find(parent, edge[1])
            if i != j:
                n = n + 1
                g_mst[edge[1]].append([edge[0],edge[2],edge[3]])
                g_mst[edge[0]].append([edge[1],edge[2],edge[3]])
                self.union(parent, rank, i, j)
        return g_mst
    
    def get_path_with_power_kruskal(self, src, dest, power):
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
            if visites[i-1]==False:           
                visites[i-1] = True
                for j in self.kruskal[i]:        
                    path2 = path.copy()
                    if j[0] in cc and not visites[j[0]-1]:       
                        if j[0]==dest and power>=j[1] :
                            path.append(dest)
                            return path                    
                        if power>=j[1]:
                            path2.append(j[0])
                            trajets.append(path2)              
        return None
    
    
    def min_power_kruskal1(self, src, dest) : 
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
        possible = lambda power: self.get_path_with_power_kruskal(src, dest, power) != None

        while not possible(max) :
            max *= 10
        
        cpt=0
        while max - min > 1 and cpt <= 50: 
            pow = int((max+min)/2)
            if possible(pow) : max = pow
            else : min = pow
            cpt+=1

        return [self.get_path_with_power(src, dest, max), max]
    
    
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


                






    
