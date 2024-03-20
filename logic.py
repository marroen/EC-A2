from chromosome import Chromosome
from graph_tool.all import *
import random
from Vertex import Vertex


def init(graph_str):
    print("init")
    graph = create_graph_from_str(graph_str)

    main_list, list_0, list_1, pointer_0, pointer_1 = fm(graph)

    draw_graph(graph, "two-nodes-color1.pdf")

    multistart_ls(main_list, list_0, list_1, pointer_0, pointer_1)
    iterated_ls(main_list, list_0, list_1, pointer_0, pointer_1)
    genetic_ls(main_list, list_0, list_1, pointer_0, pointer_1)

    draw_graph(graph, "two-nodes-color2.pdf")

    return Graph()


def draw_graph(graph, string):
    graph_draw(
        graph,
        vertex_text=graph.vertex_index,
        vertex_fill_color=graph.vertex_properties["color"],
        output=string)


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

    return setup_main_list(graph)

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


def multistart_ls(main_list, list_0, list_1, pointer_0, pointer_1):
    print("mls")


def iterated_ls(main_list, list_0, list_1, pointer_0, pointer_1):
    print("ils")


def genetic_ls(main_list, list_0, list_1, pointer_0, pointer_1):
    print("gls")


def setup_main_list(graph):
    # Here I set up the entire main_list meaning I determine:
    # vertex number
    # partitioning (0 or 1)
    # gain
    # connected vertex
    # predecessor
    # successor

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
    pointer_0 = -100
    pointer_1 = -100

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
            if gain > pointer_0:
                pointer_0 = gain

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
            if gain > pointer_0:
                pointer_1 = gain

    # print(main_list)
    # print(list_0)
    # print(list_1)

    return main_list, list_0, list_1, pointer_0, pointer_1


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

"""    
for i in range(0, 500):
        if i%2 == 0:                                                                        #Flipping 0,1,0,1...
            to_be_flipped_number = list_0[pointer_0]                                        #Determining what to flip
            main_list[to_be_flipped_number].partitioning = 1                                #Flipping

            neighbours = main_list[to_be_flipped_number].connected_vertexes                         #Updating neighbours
            random.shuffle(neighbours)                                                      #Keep unbiased
            for neighbour in neighbours:
                if (main_list[neighbour].successor is None and                              #The neighbour is on top
                    main_list[neighbour].predecessor is not None):
                    if main_list[neighbour].partitioning == 0:
                        list_0[main_list[neighbour].gain] = main_list[neighbour].predecessor#Make the pred the top
                    else:
                        list_1[main_list[neighbour].gain] = main_list[neighbour].predecessor#Make the pred the top
                    main_list[main_list[neighbour].predecessor].successor = None            #Update suc of the pred
                    main_list[neighbour].predecessor = None                                 #Resetting pred of neighbour

                elif (main_list[neighbour].predecessor is None and                          #The neighbour is below
                      main_list[neighbour].successor is not None):
                    main_list[main_list[neighbour].successor].predecessor = None            #Update pred of the suc
                    main_list[neighbour].successor = None                                   #Resetting suc of neighbour

                elif (main_list[neighbour].predecessor is None and                          #The neighbour is below
                      main_list[neighbour].successor is None):
                    if main_list[neighbour].partitioning == 0:
                        list_0[main_list[neighbour].gain] = -1
                    else:
                        list_1[main_list[neighbour].gain] = -1

                else:
                    main_list[main_list[neighbour].successor].predecessor = main_list[neighbour].predecessor
                    main_list[main_list[neighbour].predecessor].successor = main_list[neighbour].successor
                    main_list[neighbour].successor = None
                    main_list[neighbour].predecessor = None

                if main_list[neighbour].partitioning == 0:
                    main_list[neighbour].gain += 2                                          #Changing gain of neighbour
                    if main_list[neighbour].gain > pointer_0:                               #updating pointer if needed
                        pointer_0 = main_list[neighbour].gain
                    if list_0[main_list[neighbour].gain] != -1:
                        main_list[neighbour].predecessor = list_0[main_list[neighbour].gain]
                        main_list[list_0[main_list[neighbour].gain]].successor = main_list[neighbour].vertex_number
                    list_0[main_list[neighbour].gain] = main_list[neighbour].vertex_number                #putting the neighbour on top

                    if main_list[to_be_flipped_number].predecessor is not None:
                        list_0[main_list[to_be_flipped_number].gain - 2] = main_list[to_be_flipped_number].predecessor
                        main_list[main_list[to_be_flipped_number].predecessor].successor = None
                        main_list[to_be_flipped_number].predecessor = None
                    else:
                        list_0[main_list[to_be_flipped_number].gain - 2] = -1

                    if list_0[main_list[to_be_flipped_number].gain] != -1:
                        main_list[to_be_flipped_number].predecessor = list_0[main_list[to_be_flipped_number].gain]
                        main_list[list_0[main_list[to_be_flipped_number].gain]].successor = main_list[to_be_flipped_number].vertex_number
                    list_0[main_list[to_be_flipped_number].gain] = main_list[to_be_flipped_number].vertex_number

                if main_list[neighbour].partitioning == 1:
                    main_list[neighbour].gain -= 2                                          #Changing gain of neighbours
                    if list_1[main_list[neighbour].gain] != -1:
                        main_list[neighbour].predecessor = list_1[main_list[neighbour].gain]
                        main_list[list_1[main_list[neighbour].gain]].successor = main_list[neighbour].vertex_number
                    list_1[main_list[neighbour].gain] = main_list[neighbour].vertex_number

                    if main_list[to_be_flipped_number].predecessor is not None:
                        list_1[main_list[to_be_flipped_number].gain - 2] = main_list[to_be_flipped_number].predecessor
                        main_list[main_list[to_be_flipped_number].predecessor].successor = None
                        main_list[to_be_flipped_number].predecessor = None
                    else:
                        list_1[main_list[to_be_flipped_number].gain - 2] = -1

                    if list_1[main_list[to_be_flipped_number].gain] != -1:
                        main_list[to_be_flipped_number].predecessor = list_1[main_list[to_be_flipped_number].gain]
                        main_list[list_1[main_list[to_be_flipped_number].gain]].successor = main_list[to_be_flipped_number].vertex_number
                    list_1[main_list[to_be_flipped_number].gain] = main_list[to_be_flipped_number].vertex_number

            main_list[to_be_flipped_number].gain = -1*main_list[to_be_flipped_number].gain  #Updating gain

        else:
            to_be_flipped_number = list_1[pointer_1]  # Determining what to flip
            main_list[to_be_flipped_number].partitioning = 0  # Flipping

            neighbours = main_list[to_be_flipped_number].connected_vertexes  # Updating neighbours
            random.shuffle(neighbours)  # Keep unbiased
            for neighbour in neighbours:
                if (main_list[neighbour].successor is None and  # The neighbour is on top
                        main_list[neighbour].predecessor is not None):
                    if main_list[neighbour].partitioning == 0:
                        list_0[main_list[neighbour].gain] = main_list[neighbour].predecessor  # Make the pred the top
                    else:
                        list_1[main_list[neighbour].gain] = main_list[neighbour].predecessor  # Make the pred the top
                    main_list[main_list[neighbour].predecessor].successor = None  # Update suc of the pred
                    main_list[neighbour].predecessor = None  # Resetting pred of neighbour

                elif (main_list[neighbour].predecessor is None and  # The neighbour is below
                      main_list[neighbour].successor is not None):
                    main_list[main_list[neighbour].successor].predecessor = None  # Update pred of the suc
                    main_list[neighbour].successor = None  # Resetting suc of neighbour

                elif (main_list[neighbour].predecessor is None and  # The neighbour is below
                      main_list[neighbour].successor is None):
                    if main_list[neighbour].partitioning == 0:
                        list_0[main_list[neighbour].gain] = -1
                    else:
                        list_1[main_list[neighbour].gain] = -1

                else:
                    main_list[main_list[neighbour].successor].predecessor = main_list[neighbour].predecessor
                    main_list[main_list[neighbour].predecessor].successor = main_list[neighbour].successor
                    main_list[neighbour].successor = None
                    main_list[neighbour].predecessor = None

                if main_list[neighbour].partitioning == 1:
                    main_list[neighbour].gain += 2  # Changing gain of neighbour
                    if main_list[neighbour].gain > pointer_1:  # updating pointer if needed
                        pointer_1 = main_list[neighbour].gain
                    if list_1[main_list[neighbour].gain] != -1:
                        main_list[neighbour].predecessor = list_1[main_list[neighbour].gain]
                        main_list[list_1[main_list[neighbour].gain]].successor = main_list[neighbour].vertex_number
                    list_1[main_list[neighbour].gain] = main_list[neighbour].vertex_number  # putting the neighbour on top

                    if main_list[to_be_flipped_number].predecessor is not None:
                        list_1[main_list[to_be_flipped_number].gain - 2] = main_list[to_be_flipped_number].predecessor
                        main_list[main_list[to_be_flipped_number].predecessor].successor = None
                        main_list[to_be_flipped_number].predecessor = None
                    else:
                        list_1[main_list[to_be_flipped_number].gain - 2] = -1

                    if list_1[main_list[to_be_flipped_number].gain] != -1:
                        main_list[to_be_flipped_number].predecessor = list_1[main_list[to_be_flipped_number].gain]
                        main_list[list_1[main_list[to_be_flipped_number].gain]].successor = main_list[
                            to_be_flipped_number].vertex_number
                    list_1[main_list[to_be_flipped_number].gain] = main_list[to_be_flipped_number].vertex_number

                if main_list[neighbour].partitioning == 0:
                    main_list[neighbour].gain -= 2  # Changing gain of neighbours
                    if list_0[main_list[neighbour].gain] != -1:
                        main_list[neighbour].predecessor = list_0[main_list[neighbour].gain]
                        main_list[list_0[main_list[neighbour].gain]].successor = main_list[neighbour].vertex_number
                    list_0[main_list[neighbour].gain] = main_list[neighbour].vertex_number

                    if main_list[to_be_flipped_number].predecessor is not None:
                        list_0[main_list[to_be_flipped_number].gain - 2] = main_list[to_be_flipped_number].predecessor
                        main_list[main_list[to_be_flipped_number].predecessor].successor = None
                        main_list[to_be_flipped_number].predecessor = None
                    else:
                        list_0[main_list[to_be_flipped_number].gain - 2] = -1

                    if list_0[main_list[to_be_flipped_number].gain] != -1:
                        main_list[to_be_flipped_number].predecessor = list_0[main_list[to_be_flipped_number].gain]
                        main_list[list_0[main_list[to_be_flipped_number].gain]].successor = main_list[
                            to_be_flipped_number].vertex_number
                    list_0[main_list[to_be_flipped_number].gain] = main_list[to_be_flipped_number].vertex_number

            main_list[to_be_flipped_number].gain = -1 * main_list[to_be_flipped_number].gain  # Updating gain
            # ToDo: pointer!!! while list_0/1 = -1 keep dropping
"""
