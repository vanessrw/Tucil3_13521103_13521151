# import numpy as np
# import networkx as nx

# def convertToGraph(filename) :
#     # Read adjacency matrix from file
#     with open(filename) as f:
#         matrix = [[int(x) for x in line.split()] for line in f]

#     # Create graph and add edges with weights
#     G = nx.Graph()
#     for i, row in enumerate(matrix):
#         for j, weight in enumerate(row):
#             if weight > 0:
#                 G.add_edge(i, j, weight=weight)

#     # Convert graph to list of edges without 'weight' key
#     edges = G.edges(data='weight')

#     return edges

def convertToInit(filename, graph, node, matrix) :
    # Read the adjacency matrix from the file
    with open(filename, 'r') as f:
        data = f.readlines()

    # Loop through each line of the file
    for line in data:
        # Strip the newline character and split the values by whitespace
        values = line.strip().split()

        # Append the values to the matrix list as integers
        matrix.append([int(x) for x in values])

        # Create a dictionary entry for the node and its edges
        edges = {}
        for i in range(len(values)):
            if int(values[i]) != 0:
                edges[i+1] = int(values[i])
        graph[len(matrix)] = edges

        # Append the node to the node list
        node.append(len(matrix))

    # Output the initialized graph, matrix, and node
