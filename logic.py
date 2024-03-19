from chromosome import Chromosome
from graph_tool.all import *
import random
from Vertex import Vertex


def init(graph_str):
    print("init")
    graph = create_graph_from_str(graph_str)

    main_list, list_0, list_1 = fm(graph)

    multistart_ls(main_list, list_0, list_1)
    iterated_ls(main_list, list_0, list_1)
    genetic_ls(main_list, list_0, list_1)

    draw_graph(graph)

    return Graph()


def draw_graph(graph):
    graph_draw(
        graph,
        vertex_text=graph.vertex_index,
        vertex_fill_color=graph.vertex_properties["color"],
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
            if graph.edge(i, int(vertex_str[3 + j]) - 1) is None:
                graph.add_edge(i, int(vertex_str[3 + j]) - 1)

    return graph


def fm(graph):
    print("fm")
    # partition graph (not the arrays)
    a, b = partition(graph)

    print(len(a))
    print(len(b))

    return setup_main_list(a, b, graph)

    # compute gains
    # gain = v.neighbors in B (A) - v.neighbors in A (B)


def partition(graph):
    a = set()
    b = set()

    # assign property categories
    graph.vertex_properties["color"] = graph.new_vp("string")
    vcolor = graph.vertex_properties["color"]

    shuffled_vertices = list(graph.vertices())
    random.shuffle(shuffled_vertices)

    # distribute vertices evenly and assign property per vertex
    for i in range(0, len(shuffled_vertices)):
        curr_v = shuffled_vertices[i]
        if i % 2 == 0:
            a.add(curr_v)
            vcolor[curr_v] = "#1c71d8"
        else:
            b.add(curr_v)
            vcolor[curr_v] = "#2ec27e"
        i += 1

    return (a, b)


def multistart_ls(main_list, list_0, list_1):
    print("mls")


def iterated_ls(main_list, list_0, list_1):
    print("ils")


def genetic_ls(main_list, list_0, list_1):
    print("gls")


def setup_main_list(a, b, graph):
    main_list = []
    for i in range(0, 500):
        if graph.vertex_properties["color"][graph.vertex(i)] == "#1c71d8":  # ToDo: works?
            main_list.append(Vertex(i, 0, [int(n) for n in graph.vertex(i).all_neighbors()]))
        if graph.vertex_properties["color"][graph.vertex(i)] == "#2ec27e":  # ToDo: works?
            main_list.append(Vertex(i, 1, [int(n) for n in graph.vertex(i).all_neighbors()]))

    list_0 = {i: -1 for i in range(-30, 31)}
    list_1 = {i: -1 for i in range(-30, 31)}

    numbers = list(range(0, 500))
    random.shuffle(numbers)

    for j in range(0, 500):
        i = numbers[j]
        gain = 0
        if main_list[i].partitioning == 0:
            if len(main_list[i].connected_vertexes) > 0:
                for n in main_list[i].connected_vertexes:
                    if main_list[n].partitioning == 0:
                        gain -= 1
                    if main_list[n].partitioning == 1:
                        gain += 1
            if list_0[gain] == -1:
                list_0[gain] = i
                main_list[i].gain = gain
            else:
                previous_number = list_0[gain]
                main_list[previous_number].successor = i
                main_list[i].predecessor = previous_number
                main_list[i].gain = gain
                list_0[gain] = i

        else:
            if len(main_list[i].connected_vertexes) > 0:
                for n in main_list[i].connected_vertexes:
                    if main_list[n].partitioning == 1:
                        gain -= 1
                    if main_list[n].partitioning == 0:
                        gain += 1
            if list_1[gain] == -1:
                list_1[gain] = i
                main_list[i].gain = gain
            else:
                previous_number = list_1[gain]
                main_list[previous_number].successor = i
                main_list[i].predecessor = previous_number
                main_list[i].gain = gain
                list_1[gain] = i

    # print(main_list)
    # print(list_0)
    # print(list_1)

    return main_list, list_0, list_1


# Ignore, this is old stuff of yoav, but I want to keep it in for now

"""
    # List with a tuple
    # 0 = # of vertex
    # 1 = partitioning (0 or 1)
    # 2 = gain
    # 3 = connected vertex
    # 4 = predecessor
    # 5 = successor
    
    main_list = []
    for i in range(0, 500):
        if i in a:
            tup = [i, 0, None, [int(n) for n in graph.vertex(i).all_neighbors()], None, None]
            main_list.append(tup)
        if i in b:
            tup = [i, 1, None, [int(n) for n in graph.vertex(i).all_neighbors()], None, None]
            main_list.append(tup)
            
    for j in reversed(range(0, 500)):
        i = numbers[j]
        gain = 0
        if main_list[i][1] == 0:
            for n in main_list[i][3]:
                if main_list[n][1] == 0:
                    gain -= 1
                if main_list[n][1] == 1:
                    gain += 1
            if list_0[gain] == -1:
                list_0[gain] = i
                main_list[i][2] = gain
            else:
                previous_number = list_0[gain]
                main_list[previous_number][5] = i
                main_list[i][4] = previous_number
                main_list[i][2] = gain
        else:
            for n in main_list[i][3]:
                if main_list[n][1] == 1:
                    gain -= 1
                if main_list[n][1] == 0:
                    gain += 1
            if list_1[gain] == -1:
                list_1[gain] = i
                main_list[i][2] = gain
            else:
                previous_number = list_1[gain]
                main_list[previous_number][5] = i
                main_list[i][4] = previous_number
                main_list[i][2] = gain
"""
