from chromosome import Chromosome
from graph_tool.all import *
import random

def init(graph_str):
    print("init")
    graph = create_graph_from_str(graph_str)

    fm(graph)

    draw_graph(graph)

    return Graph()

def draw_graph(graph):
    graph_draw(
            graph,
            vertex_text=graph.vertex_index,
            vertex_fill_color = graph.vertex_properties["color"],
            output="two-nodes-color.pdf")

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
    a, b = partition(graph)
    
    # compute gains
    # gain = v.neighbors in B (A) - v.neighbors in A (B)


def partition(graph):
    a = []
    b = []
    
    # assign property categories
    graph.vertex_properties["color"] = graph.new_vp("string")
    vcolor = graph.vertex_properties["color"]

    shuffled_vertices = list(graph.vertices())
    random.shuffle(shuffled_vertices)

    # distribute vertices evenly and assign property per vertex
    for i in range(0, len(shuffled_vertices)):
        curr_v = shuffled_vertices[i]
        if i % 2 == 0:
            a.append(curr_v)
            vcolor[curr_v] = "#1c71d8"
        else:
            b.append(curr_v)
            vcolor[curr_v] = "#2ec27e"
        i += 1

    return (a, b)

def multistart_ls():
    print("mls")

def iterated_ls():
    print("ils")

def genetic_ls():
    print("gls")
