from chromosome import Chromosome
from graph_tool.all import *

def init(graph_str):
    print("init")
    graph = create_graph_from_str(graph_str)
    print(graph)
    for edge in graph.get_edges():
        print(edge)
    return Graph()

def create_graph_from_str(graph_str):
    # create graph based on textfile
    splitted_lines = graph_str.split("\n")
    graph = Graph(g=500, directed=False)
    for i in range(0, 500):
        vertex_str = splitted_lines[i].split()
        n = int(vertex_str[2])
        for j in range(0, n):
            graph.add_edge(i,int(vertex_str[3+j])-1)
    
    return graph

def fm(graph):
    print("fm")
    # partition graph

def multistart_ls():
    print("mls")

def iterated_ls():
    print("ils")

def genetic_ls():
    print("gls")
