import heapq
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    cost: int
    node: Any=field(compare=False)
    path: Any=field(compare=False)

# Calculate the shortest path using UCS
def ucs(graph, start, dest, name):
    iteration = 0
    visited = set()
    queue = [PrioritizedItem(0, start, [])]
    while queue:
        iteration += 1
        item = heapq.heappop(queue)
        cost, node, path = item.cost, item.node, item.path
        
        if node not in visited:
            visited.add(node)
            path = path + [name[node]]
            
            if node == dest:
                return (iteration, cost, path)
            
            for neighbor, weight in enumerate(graph[node]):
                if weight != 0 and neighbor not in visited:
                    actual_cost = cost + weight
                    heapq.heappush(queue, PrioritizedItem(actual_cost, neighbor, path))
    return (iteration, float("inf"), [])

# Calculate the shortest path using A*
def astar(graph, start, dest, name):
    iteration = 0
    visited = set()
    queue = [PrioritizedItem(0, start, [])]
    heuristic = [0] * len(graph)
    
    while queue:
        iteration += 1
        item = heapq.heappop(queue)
        cost, node, path = item.cost, item.node, item.path
        if node not in visited:
            visited.add(node)
            path = path + [name[node]]
            if node == dest:
                # if shortest path is found, return the iteration count, cost, and path
                return (iteration, cost, path)
            if (node != start):
                heuristic[node] = cost - heuristic[node]
            for neighbor in range(len(graph[node])):
                if graph[node][neighbor] != 0 and neighbor not in visited:
                    # Calculate the actual cost f(n) = g(n) + h(n)
                    actual_cost = cost + graph[node][neighbor] + heuristic[neighbor]
                    heapq.heappush(queue, PrioritizedItem(actual_cost, neighbor, path))
    # if no path is found, return the iteration count, infinity, and empty path
    return (iteration, float("inf"), [])

