import os
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def is_valid_input_format(filename):
    with open(filename, 'r') as f:
        try:
            # read the first line containing the number of nodes
            num_nodes = int(f.readline().strip())

            # read the remaining lines containing the nodes' coordinates and names
            for i in range(num_nodes):
                line = f.readline().strip()
                if len(line.split()) != 3:
                    return False

            # read the adjacency matrix lines
            for i in range(num_nodes):
                line = f.readline().strip()
                if len(line.split()) != num_nodes:
                    return False

            # if all lines were read successfully, the format is valid
            return True

        except ValueError:
            # if there is an error while reading the file, the format is invalid
            return False


def parse_input_file(filepath):
    # read input file
    file_path = os.path.join('test', filepath)
    with open(file_path) as f:
        n = int(f.readline().strip())
        coords = {}
        for i in range(n):
            lat, long, name = f.readline().strip().split()
            coords[i] = {'name': name, 'lat': float(lat), 'long': float(long)}
        graph = [[int(x) for x in line.strip().split()] for line in f.readlines()]

    name_to_index = {coords[i]['name']: i for i in range(n)}
    index_to_name = {i: coords[i]['name'] for i in range(n)}
    result = [[0 for j in range(n)] for i in range(n)]

    for i in range(n):
        for j in range(n):
            if graph[i][j] == 1:
                result[i][j] = ((coords[i]['lat'] - coords[j]['lat']) ** 2 + 
                                (coords[i]['long'] - coords[j]['long']) ** 2) ** 0.5
            else:
                result[i][j] = 0

    # write the result to a new file
    filename = 'parsed.txt'
    parsed_file_path = 'test/parsed.txt'
    with open(parsed_file_path, 'w') as f:
        f.write(','.join(index_to_name[i] for i in range(n)) + '\n')
        for i in range(n):
            f.write(' '.join(str(x) for x in result[i]) + '\n')
    return filename


# ----- INPUT -----
def inputFile():
    while True:

        # open file (from file explorer)
        root = Tk()
        root.withdraw()
        filepath = askopenfilename(initialdir=os.path.join(os.path.dirname(__file__), '..', 'test'),
                                   title="Select Input File",
                                   filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        root.destroy()
        if is_valid_input_format(filepath):
            # if format is valid, parse the file
            f = parse_input_file(filepath)
            # print("File parsed successfully.")
        try:
            # with open(filepath, 'r') as f:
                # nodes namea
                line = f.readline()
                name = [str(x) for x in line.strip().split(',')]
                size = len(name)
                if size < 8:
                    raise ValueError("err: File must contain at least 8 nodes")
                
                # adjacency matrix
                matrix = []
                for i in range(size):
                    line = f.readline()
                    row = line.strip().split()

                    if len(row) != size:
                        raise ValueError("err: the adjacency matrix must be rectangular.")
                    # check all elements are non negative
                    try:
                        row = [float(element) for element in row]
                        if any(element < 0 for element in row):
                            raise ValueError("err: elements must be non-negative integers")
                        matrix.append(row)
                    except ValueError:
                        raise ValueError("err: elements must be integers")
                
                # check if matrix symmetric
                for i in range(size):
                    for j in range(i+1, size):
                        if matrix[i][j] != matrix[j][i]:
                            raise ValueError("The adjacency matrix is not symmetric.")
            
                return name, matrix
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}")
            continue
        
def ubahGraf(filepath):
    try:       
        with open(filepath, 'r') as f:
            # nodes name
            line = f.readline()
            name = [str(x) for x in line.strip().split(',')]
            size = len(name)
            if size < 8:
                raise ValueError("err: File must contain at least 8 nodes")

            # adjacency matrix
            matrix = []
            for i in range(size):
                line = f.readline()
                row = line.strip().split()

                if len(row) != size:
                    raise ValueError("err: the adjacency matrix must be rectangular.")
                # check all elements are non negative
                try:
                    row = [float(element) for element in row]
                    if any(element < 0 for element in row):
                        raise ValueError("err: elements must be non-negative integers")
                    matrix.append(row)
                except ValueError:
                    raise ValueError("err: elements must be integers")

            # check if matrix symmetric
            for i in range(size):
                for j in range(i+1, size):
                    if matrix[i][j] != matrix[j][i]:
                        raise ValueError("The adjacency matrix is not symmetric.")

            return matrix
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return None

# get user input node
def inputRequest(name):
    print("-----------------------------")
    print("nodes :")
    for i, node in enumerate(name, start=1):
        print(f"{i}. {node.strip()}")
    
    # starting node
    while True:
        try:
            input_node = int(input("starting node : "))
            if input_node < 1 or input_node > len(name):
                print("starting node not valid !")
                continue
            start_node = input_node - 1
            break
        except ValueError:
            print("input not valid !")
    
    print("-----------------------------")
    print("valid nodes:")
    for i, node in enumerate(name):
        if i < start_node:
            print(f"{i+1}.{node}")
        elif i > start_node:
            print(f"{i}.{node}")
    
    # destination node
    while True:
        try:
            input_node = int(input("destination node : "))
            if input_node < 1 or input_node > len(name) - 1:
                print("destination node not valid !")
                continue
            end_node = input_node - 1 if input_node - 1 < start_node else input_node
            break
        except ValueError:
            print("input not valid ")

    return start_node, end_node


# # ----- OUTPUT -----
# def plot(graph, name, path):
#     # vertex labels
#     labels = {k: v for k, v in enumerate(name)}

#     # Convert adjacency matrix to weighted graph
#     G = nx.Graph()
#     for i in range(len(graph)):
#         for j in range(i+1, len(graph[i])):
#             if graph[i][j] != 0:
#                 G.add_edge(labels[i], labels[j], weight=graph[i][j])

#     # Plot weighted graph
#     pos = nx.spring_layout(G)
#     nx.draw(G, pos, with_labels=True, font_weight='bold', font_color='black', node_color = 'pink') #bulet" nodesnya
#     edge_labels = nx.get_edge_attributes(G, 'weight')
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_weight='bold') #weight angka ditengah" rute
#     edge_colors = ['black' if (path[i], path[i+1]) in nx.edges(G) else 'k' for i in range(len(path)-1)]
#     nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i+1]) for i in range(len(path)-1)], edge_color='pink', width=5)
#     nx.draw_networkx_edges(G, pos, edge_color=edge_colors)
#     plt.show()

def plot(graph, name, path, filename):
    plt.clf()
    # vertex labels
    labels = {k: v for k, v in enumerate(name)}

    # Convert adjacency matrix to weighted graph
    G = nx.Graph()
    for i in range(len(graph)):
        for j in range(i+1, len(graph[i])):
            if graph[i][j] != 0:
                G.add_edge(labels[i], labels[j], weight=graph[i][j])

    # Plot weighted graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', font_color='black', node_color = 'pink') #bulet" nodesnya
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_weight='bold') #weight angka ditengah" rute
    edge_colors = ['black' if (path[i], path[i+1]) in nx.edges(G) else 'k' for i in range(len(path)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i+1]) for i in range(len(path)-1)], edge_color='pink', width=5)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors)
    # set the path to the directory where you want to save the file
    save_dir = 'static'
    
    # concatenate the directory and filename to create the full path to the file
    filepath = os.path.join(save_dir, filename)

    # save the image to the specified directory
    plt.savefig(filepath)
    return filepath


def result(function, name, start, end, iteration, cost, path, time):
    print(f"--------------------------------------")
    print(f"         {function} Algorithm         ")
    print(f"  Start node: {name[start]}")
    print(f"  End node: {name[end]}")
    print(f"  Shortest path: {path}")
    print(f"  Shortest distance: {cost}")
    print(f"  Elapsed time: {time} ms")
    print(f"  With {iteration}x iteration     ")