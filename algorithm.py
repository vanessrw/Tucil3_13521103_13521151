import math
from queue import PriorityQueue

class Graph:
    def __init__(self, filename):
        self.nodes = []
        self.edges = []
        self.graph = {}
        self.adj_matrix = []

    def read_graph(self, filename):
        # Read file and store data
        with open(filename, 'r') as f:
            data = f.readlines()[1:]
            for line in data:
                node = line.strip().split()
                self.nodes.append(node[2])
                self.graph[node[2]] = (float(node[0]), float(node[1]))

        # Create adjacency matrix
        num_nodes = len(self.nodes)
        self.adj_matrix = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]

        # Calculate distances and fill in matrix
        for i in range(num_nodes):
            for j in range(num_nodes):
                if i != j:
                    dist = self.eucDist(self.nodes[i], self.nodes[j])
                    self.adj_matrix[i][j] = dist
                    
    
    def write_matrix(self, filename):
        with open(filename, 'w') as f:
            for row in self.graph:
                f.write(' '.join(map(str, row)) + '\n')

    def eucDist(self, s1, s2):
        # latitude and longitude
        lat1, lon1 = self.graph[s1][:2]
        lat2, lon2 = self.graph[s2][:2]

        # source : https://community.esri.com/t5/coordinate-reference-systems/distance-on-a-sphere-the-haversine-formula/ba-p/902128
        R = 6371000  # radius of Earth in meters
        phi_1 = math.radians(lat1)
        phi_2 = math.radians(lat2)

        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        meters = R * c  # output distance in meters
        meters = round(meters, 3)

        return meters

    def astar(self, start, goal):
        active_list = [[self.eucDist(start, goal), [start]]]
        while len(active_list) > 0:
            element = active_list[0]
            if element[1][-1] == goal:
                return element
            else:
                new = self.generate(element, goal)
                active_list.pop(0)
                active_list.extend(new)
                active_list.sort(key=self.sort_helper)
        return ["path not found", [goal]]

    # contoh astar
    # obstacles = [
    #     [0, 0, 0, 0, 0],
    #     [0, 1, 1, 0, 0],
    #     [0, 0, 1, 0, 0],
    #     [0, 0, 0, 0, 1],
    #     [0, 0, 0, 1, 0]
    # ]

    # grid = Grid(obstacles)
    # start = (0, 0)
    # goal = (4, 4)
    # path = grid.astar(start, goal)

    # print(path) 
    # Output: [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]

    def ucs(self, start, goal):
        visited = set()
        queue = PriorityQueue()
        queue.put((0, [start]))
        
        while not queue.empty():
            cost, path = queue.get()
            node = path[-1]
            
            if node == goal:
                return (path, cost)
            
            if node not in visited:
                visited.add(node)
                
                for neighbor, neighbor_cost in self.graph[node].items():
                    if neighbor not in visited:
                        new_path = list(path)
                        new_path.append(neighbor)
                        new_cost = cost + neighbor_cost
                        queue.put((new_cost, new_path))
        
        return (["dead end"], 0)

    # contoh ucs
    # graph = {
    #     'A': {'B': 1, 'C': 4},
    #     'B': {'C': 2, 'D': 5},
    #     'C': {'D': 1},
    #     'D': {}
    # }

    # matrix = {}

    # g = Graph(graph, matrix)

    # path, cost = g.ucs('A', 'D')
    # print("Shortest path:", path)
    # print("Shortest cost:", cost)

    # output
    # Shortest path: ['A', 'B', 'D']
    # Shortest cost: 6

    def generate(self, element, simpulTujuan):
        hasil = []
        g = self.totalDistance(element[1])
        x = self.node.index(element[1][-1])
        for i, node in enumerate(self.node):
            if self.matrix[x][i] == 1:
                temp = element[1][:]
                if node not in temp:
                    temp.append(node)
                    h = self.EucDist(element[1][-1], node) + self.EucDist(node, simpulTujuan)
                    f = g + h
                    hasil.append([f, temp])
        return hasil

    def totalDistance(self, l): # jarak total
        if len(l) <= 1:
            return 0
        else:
            s = sum(self.EucDist(l[i-1], l[i]) for i in range(1, len(l)))
            return s


    def sorting(self, element):
        return element[0]
