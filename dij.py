#!/usr/bin/env python3.6

import heapq
import math
import sys
from typing import Dict, List, Tuple

import pydot

Matrix = Dict[str, List[Tuple[str, float]]]


def build_matrix(edges: List[pydot.Edge]) -> Matrix:
    matrix = {}
    for e in edges:
        src = e.get_source()
        dst = e.get_destination()
        dist = float(e.get_attributes()["length"])

        if src in matrix.keys():
            matrix[src].append((dst, dist))
        else:
            matrix[src] = [(dst, dist)]

        if e.get_parent_graph().get_top_graph_type() == "graph":
            if dst in matrix.keys():
                matrix[dst].append((src, dist))
            else:
                matrix[dst] = [(src, dist)]

    return matrix


def dijkstra(matrix: Matrix, source: str, target: str = None) \
        -> Tuple[Dict[str, List[str]], Dict[str, int]]:

    queue = []
    distances = {}
    trees = {}

    distances[source] = 0.0
    heapq.heappush(queue, (0.0, source))

    unvisited = set(vrtx for row in matrix.items() for
                    subsets in [row[0]] + [subvrtx[0]
                                           for subvrtx in row[1]] for
                    vrtx in subsets)

    while unvisited:
        u = heapq.heappop(queue)[1]

        if u not in unvisited:
            continue

        unvisited.remove(u)

        if u == target:
            break

        if u in matrix:
            for n in matrix[u]:
                v, d = n
                alt = distances.get(u, math.inf) + d
                if alt < distances.get(v, math.inf):
                    distances[v] = alt
                    heapq.heappush(queue, (alt, v))
                    trees[v] = [u]
                elif alt == distances[v]:
                    trees[v].append(u)

    return (trees, distances)


def update_graph(graph: pydot.Graph,
                 trees: Dict[str, List[str]],
                 current: str) -> None:

    if current in trees:
        for p in trees[current]:
            update_graph(graph, trees, p)

            e = graph.get_edge(p, current)[0]
            e.get_attributes()['color'] = "darkgreen"
            e.get_attributes()['style'] = "bold"

    n = graph.get_node(current)[0].get_attributes()
    n['fillcolor'] = "green"
    n['style'] = "filled"


def decorate_graph(graph: pydot.Graph, source: str, destination: str,
                   distance: Dict[str, int]) -> None:

    for edge in graph.get_edges():
        edge.get_attributes()['label'] = edge.get_attributes()['length']

    for node in graph.get_nodes():
        n = node.get_name()
        if n in distance:
            node.get_attributes()['label'] \
                    = '"' + n + ":" + str(distance[n]) + '"'

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

        matrix = build_matrix(graph.get_edges())
        trees, distances = dijkstra(matrix, source, destination)
        update_graph(graph, trees, destination)
        decorate_graph(graph, source, destination, distances)

        print(graph)


if __name__ == "__main__":
    main()
