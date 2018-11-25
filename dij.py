#!/usr/bin/env python3.6

import pydot
import math
import sys
import heapq
from typing import List, Dict, Set, Tuple


def build_neighbours(edges: List[pydot.Edge]) \
        -> Dict[str, List[Tuple[str, float]]]:
    neighbours = {}
    for e in edges:
        src = e.get_source()
        dst = e.get_destination()
        dist = float(e.get_attributes()["length"])

        if src in neighbours.keys():
            neighbours[src].append((dst, dist))
        else:
            neighbours[src] = [(dst, dist)]

        if e.get_parent_graph().get_top_graph_type() == "graph":
            if dst in neighbours.keys():
                neighbours[dst].append((src, dist))
            else:
                neighbours[dst] = [(src, dist)]

    return neighbours

# Helper for naive implementation
def get_next_vertex(unvisited: Set[str], distance: Dict[str, float]) -> str:
    d = {n: distance[n] for n in unvisited}
    return min(d, key=d.get)


# Helper for priority queue
def dec_priority(queue: List[Tuple[float, str]], name: str, value: float):
    for n in queue:
        if n[1] == name:
            queue.remove(n)
            heapq.heapify(queue)
            heapq.heappush(queue, (value, name))
            return

    raise Exception("No such element in heap")


def dijkstra(graph: pydot.Graph, source: str, target: str = None) \
        -> Tuple[Dict[str, List[str]], Dict[str, int]]:

    # unvisited = set()
    unvisited = []
    distance = {}
    previous = {}

    neighbours = build_neighbours(graph.get_edges())
    for node in graph.get_nodes():
        name = node.get_name()
        previous[name] = []

        if name != source:
            distance[name] = math.inf
            # unvisited.add(name)
            heapq.heappush(unvisited, (math.inf, name))

    distance[source] = 0.0
    # unvisited.add(source)
    heapq.heappush(unvisited, (0.0, source))

    while len(unvisited) > 0:
        # u = get_next_vertex(unvisited, distance)
        # unvisited.remove(u)
        u = heapq.heappop(unvisited)[1]

        if u == target:
            break

        if u in neighbours:
            for n in neighbours[u]:
                v, d = n
                alt = distance[u] + d
                if alt < distance[v]:
                    distance[v] = alt
                    dec_priority(unvisited, v, alt)
                    previous[v] = [u]
                elif alt == distance[v]:
                    previous[v].append(u)

    return (previous, distance)

def update_graph(graph: pydot.Graph, previous: Dict[str, List[str]],
                 distance: Dict[str, int], current: str) -> None:

    if current in previous:
        for p in previous[current]:
            update_graph(graph, previous, distance, p)

            e = graph.get_edge(p, current)[0]
            e.get_attributes()['color'] = "darkgreen"
            e.get_attributes()['style'] = "bold"

    n = graph.get_node(current)[0].get_attributes()
    n['fillcolor'] = "green"
    n['style'] = "filled"
    n['label'] = '"' \
        + current + ":" + str(distance[current]) \
        + '"'

def decorate_graph(graph: pydot.Graph, source: str, destination: str) -> None:
    for edge in graph.get_edges():
        edge.get_attributes()['label'] = edge.get_attributes()['length']

    graph.get_node(source)[0].get_attributes()['fillcolor'] = "lightblue"
    graph.get_node(source)[0].get_attributes()['style'] = "filled"
    graph.get_node(destination)[0].get_attributes()['fillcolor'] = "pink"
    graph.get_node(destination)[0].get_attributes()['style'] = "filled"


def main():
    graphs = pydot.graph_from_dot_file("graph.dot", 'utf-8')

    for graph in graphs:
        nodes = graph.get_nodes()

        if len(sys.argv) < 3:
            raise Exception("Not enough arguments")

        source = sys.argv[1]
        destination = sys.argv[2]

        names = [n.get_name() for n in nodes]
        if source not in names:
            raise Exception("Not such node: %s" % source)
        if destination not in names:
            raise Exception("Not such node: %s" % destination)

        previous, distance = dijkstra(graph, source, destination)
        update_graph(graph, previous, distance, destination)
        decorate_graph(graph, source, destination)

        print(graph)


if __name__ == "__main__":
    main()
