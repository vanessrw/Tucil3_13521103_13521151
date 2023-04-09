from IOFile import inputFile, inputRequest, plot, result
from algorithm import astar, ucs
from timeit import timeit

def start():
    name, graph = inputFile()

    # Plot graf awal
    path = []
    plot(graph, name, path)

    start, end = inputRequest(name)

    # the shortest path UCS
    ucs_iteration, ucs_cost, ucs_path = ucs(graph, start, end, name)
    ucs_time = timeit(lambda: ucs(graph, start, end, name), number=1) * 1000
    result("UCS", name, start, end, ucs_iteration, ucs_cost, ucs_path, ucs_time)
    plot(graph, name, ucs_path)

    # shortest path A*
    astar_iteration, astar_cost, astar_path = astar(graph, start, end, name)
    astar_time = timeit(lambda: astar(graph, start, end, name), number=1) * 1000
    result("A*", name, start, end, astar_iteration, astar_cost, astar_path, astar_time)
    plot(graph, name, astar_path)

start()