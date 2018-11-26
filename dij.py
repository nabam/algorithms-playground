#!/usr/bin/env python3.6

import heapq
import math
import sys
import random
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


def cost_estimate(start: str, goal: str, score: float) -> float:
    if score == 0.0:
        return 0.0
    if start == goal:
        return 0.0
    return random.uniform(0.0, score)/2


def a_star(matrix: Matrix, source: str, target: str) \
        -> Tuple[Dict[str, List[str]], Dict[str, int]]:

    closed = set()
    open = set()
    queue = []

    hops = {}

    g_score = {}
    f_score = {}

    g_score[source] = 0.0
    f_score[source] = cost_estimate(source, target, 0.0)

    heapq.heappush(queue, (f_score[source], source))
    open.add(source)

    while queue:
        current = heapq.heappop(queue)[1]

        if current not in open:
            continue

        open.remove(current)
        closed.add(current)

        if current == target:
            break

        if current in matrix:
            for n in matrix[current]:
                neighbor, distance = n
                if neighbor in closed:
                    continue

                alt = g_score.get(current, math.inf) + distance

                if neighbor not in open:
                    open.add(neighbor)
                elif alt >= g_score.get(current, math.inf):
                    continue

                hops[neighbor] = [current]
                g_score[neighbor] = alt
                f_score[neighbor] = alt \
                    + cost_estimate(neighbor, target, alt)
                heapq.heappush(queue, (f_score[neighbor], neighbor))

    return (hops, f_score)


def dijkstra(matrix: Matrix, source: str, target: str = None) \
        -> Tuple[Dict[str, List[str]], Dict[str, int]]:

    queue = []
    distances = {}
    hops = {}
    visited = set()

    distances[source] = 0.0
    heapq.heappush(queue, (0.0, source))

    while queue:
        current = heapq.heappop(queue)[1]

        if current in visited:
            continue

        visited.add(current)

        if current == target:
            break

        if current in matrix:
            for n in matrix[current]:
                neighbor, distance = n
                alt = distances.get(current, math.inf) + distance
                if alt < distances.get(neighbor, math.inf):
                    distances[neighbor] = alt
                    heapq.heappush(queue, (alt, neighbor))
                    hops[neighbor] = [current]
                elif alt == distances[neighbor]:
                    hops[neighbor].append(current)

    return (hops, distances)


def update_graph(graph: pydot.Graph,
                 hops: Dict[str, List[str]],
                 current: str) -> None:

    if current in hops:
        for p in hops[current]:
            update_graph(graph, hops, p)

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
                = '"{0}:{1:.2f}"'.format(n, distance[n])

    graph.get_node(source)[0].get_attributes()['fillcolor'] = "lightblue"
    graph.get_node(source)[0].get_attributes()['style'] = "filled"
    graph.get_node(destination)[0].get_attributes()['fillcolor'] = "pink"
    graph.get_node(destination)[0].get_attributes()['style'] = "filled"


def main():
    if len(sys.argv) < 3:
        raise Exception("Not enough arguments")

    source = sys.argv[1]
    destination = sys.argv[2]

    graphs = pydot.graph_from_dot_file("graph.dot", 'utf-8')

    for graph in graphs:
        nodes = graph.get_nodes()

        names = [n.get_name() for n in nodes]
        if source not in names:
            raise Exception("Not such node: %s" % source)
        if destination not in names:
            raise Exception("Not such node: %s" % destination)

        matrix = build_matrix(graph.get_edges())
        hops, distances = dijkstra(matrix, source, destination)
        update_graph(graph, hops, destination)
        decorate_graph(graph, source, destination, distances)

        gname = graph.get_name()
        graph.set_name(gname + "_dijkstra")
        print(graph)

    graphs = pydot.graph_from_dot_file("graph.dot", 'utf-8')

    for graph in graphs:
        nodes = graph.get_nodes()

        matrix = build_matrix(graph.get_edges())
        hops, distances = a_star(matrix, source, destination)
        update_graph(graph, hops, destination)
        decorate_graph(graph, source, destination, distances)

        gname = graph.get_name()
        graph.set_name(gname + "_astar")
        print(graph)


if __name__ == "__main__":
    main()
