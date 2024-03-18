from chromosome import Chromosome
from graph_tool.all import *
import random

def init(graph_str):
    print("init")
    graph = create_graph_from_str(graph_str)

    fm(graph)
    return Graph()

# this is 0-based indexing, thus (textfile_index - 1)
def create_graph_from_str(graph_str):
    # create graph based on textfile
    splitted_lines = graph_str.split("\n")
    graph = Graph(g=500, directed=False)
    for i in range(0, 500):
        vertex_str = splitted_lines[i].split()
        n = int(vertex_str[2])
        for j in range(0, n):
            if graph.edge(i, int(vertex_str[3+j])-1) is None:
                graph.add_edge(i, int(vertex_str[3+j])-1)
    
    return graph

def fm(graph):
    print("fm")
    # partition graph
    a = []
    b = []
    shuffled_vertices = list(graph.vertices())
    random.shuffle(shuffled_vertices)
    for i in range(0, len(shuffled_vertices)):
        if i % 2 == 0:
            a.append(shuffled_vertices[i])
        else:
            b.append(shuffled_vertices[i])
        i += 1


def multistart_ls():
    print("mls")

def iterated_ls():
    print("ils")

def genetic_ls():
    print("gls")
