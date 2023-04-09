from IOFile import *
from algorithm import astar, ucs
from timeit import timeit

def start():
    # file = open('../test/matrix.txt', 'r')
    # test = "../test/matrix.txt"
    # line = file.readline()
    # name = [str(x) for x in line.strip().split(',')]
    # size = len(name)
    # print(size)
    # graph = ubahGraf(file)
    
    # print(name)
    filepath = "../test/weight.txt"
    graph = ubahGraf("../test/weight.txt")
    
    with open(filepath, 'r') as f:
            # nodes name
            line = f.readline()
            name = [str(x) for x in line.strip().split(',')]

    # Plot graf awal
    path = []
    plot(graph, name, path, "graphawal.png")

    start, end = inputRequest(name)

    # the shortest path UCS
    ucs_iteration, ucs_cost, ucs_path = ucs(graph, start, end, name)
    ucs_time = timeit(lambda: ucs(graph, start, end, name), number=1) * 1000
    result("UCS", name, start, end, ucs_iteration, ucs_cost, ucs_path, ucs_time)
    img = plot(graph, name, ucs_path, "ucsgraph.png")

    # shortest path A*
    astar_iteration, astar_cost, astar_path = astar(graph, start, end, name)
    astar_time = timeit(lambda: astar(graph, start, end, name), number=1) * 1000
    result("A*", name, start, end, astar_iteration, astar_cost, astar_path, astar_time)
    img = plot(graph, name, astar_path, "astargraph.png")

start()