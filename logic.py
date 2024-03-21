from copy import deepcopy

from chromosome import Chromosome
from graph_tool.all import *
import random
from Vertex import Vertex

global main_list
global main_list_best, final_main_list
global list_0, list_1
global pointer_0, pointer_1


def init(graph_str):
    global main_list, main_list_best
    global final_main_list
    print("init")
    graph = create_graph_from_str(graph_str)

# MLS --------------------------------------------------------------
    smallest_cut_size = 10000000

    for i in range(0, 20):                                          # How many resets do we want?
        fm(graph)

        if i == 0:
            draw_graph(graph, "two-nodes-color1.pdf")

        final_cut_size = multistart_ls(graph)
        if final_cut_size < smallest_cut_size:
            smallest_cut_size = final_cut_size
            final_main_list = deepcopy(main_list)

    print("")
    print(smallest_cut_size)
    new_graph(graph)
    draw_graph(graph, "two-nodes-color2.pdf")
# MLS --------------------------------------------------------------

    # fm(graph)

    # iterated_ls(main_list, list_0, list_1, pointer_0, pointer_1)
    # genetic_ls(main_list, list_0, list_1, pointer_0, pointer_1)

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

    setup_main_list(graph)

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


def new_graph(graph):
    a = set()
    b = set()
    graph.vertex_properties["color"] = graph.new_vp("string")
    vcolor = graph.vertex_properties["color"]

    for element in final_main_list:
        curr_v = element.vertex_number
        if element.partitioning == 0:
            a.add(curr_v)
            vcolor[curr_v] = "#1c71d8"
        else:
            b.add(curr_v)
            vcolor[curr_v] = "#2ec27e"


def multistart_ls(graph):
    print("mls")
    global main_list, main_list_best
    global list_0, list_1
    global pointer_0, pointer_1

    cut_size = 0
    lowest_cut_size = 1000000000
    cut_size_lowered = True

    for edge in graph.edges():
        a, b = edge
        if main_list[int(a)].partitioning != main_list[int(b)].partitioning:
            cut_size += 1

    while cut_size_lowered:
        cut_size_lowered = False
        for i in range(0, 500):
            if i % 2 == 0:                                                                  # Flipping 0,1,0,1..
                for j in reversed(range(-30, 31)):
                    if list_0[j] != -1:
                        pointer_0 = j
                        break
                new_cut_size = update_list(1, list_0, pointer_0, cut_size)
                cut_size = new_cut_size

            else:
                for j in reversed(range(-30, 31)):
                    if list_1[j] != -1:
                        pointer_1 = j
                        break
                new_cut_size = update_list(0, list_1, pointer_1, cut_size)
                if new_cut_size < lowest_cut_size:
                    main_list_best = []
                    main_list_best = deepcopy(main_list)
                    lowest_cut_size = new_cut_size
                    cut_size_lowered = True
                cut_size = new_cut_size

        if cut_size_lowered:
            main_list = []
            main_list = deepcopy(main_list_best)
            cut_size = lowest_cut_size
            reset_main_list()

    test = 0
    #print(main_list)
    print(lowest_cut_size)
    print(cut_size)
    for element in main_list:
        if element.partitioning ==1:
            test += 1
    #print(test)

    return cut_size


def update_list(new_partitioning, list_x, pointer, cut_size):
    global main_list
    global list_0, list_1

    flipped_number = list_x[pointer]                                                    # Determining what to flip

    if main_list[flipped_number].gain > 0:
        cut_size -= main_list[flipped_number].gain
    else:
        cut_size += abs(main_list[flipped_number].gain)

    main_list[flipped_number].partitioning = new_partitioning                           # Flipping

    neighbours = main_list[flipped_number].connected_vertexes                           # Updating neighbours
    random.shuffle(neighbours)                                                          # Keep unbiased

    for neighbour in neighbours:
        if main_list[neighbour].flipped == False:
            # I start by updating everything around the neighbours without updating the neighbours
            if (main_list[neighbour].successor is None and                                  # The neighbour is on top
                main_list[neighbour].predecessor is not None):
                if main_list[neighbour].partitioning == 0:
                    list_0[main_list[neighbour].gain] = main_list[neighbour].predecessor    # Make the pred the top
                else:
                    list_1[main_list[neighbour].gain] = main_list[neighbour].predecessor    # Make the pred the top
                main_list[main_list[neighbour].predecessor].successor = None                # Update suc of the pred
                main_list[neighbour].predecessor = None                                     # Resetting pred of neighbour

            elif (main_list[neighbour].predecessor is None and                              # The neighbour is below
                  main_list[neighbour].successor is not None):
                main_list[main_list[neighbour].successor].predecessor = None                # Update pred of the suc
                main_list[neighbour].successor = None                                       # Resetting suc of neighbour

            elif (main_list[neighbour].predecessor is None and                              # neighbour is alone
                  main_list[neighbour].successor is None):
                if main_list[neighbour].partitioning == 0:
                    list_0[main_list[neighbour].gain] = -1
                else:
                    list_1[main_list[neighbour].gain] = -1

            else:
                main_list[main_list[neighbour].successor].predecessor = main_list[neighbour].predecessor        # correct?
                main_list[main_list[neighbour].predecessor].successor = main_list[neighbour].successor          # correct?
                main_list[neighbour].successor = None
                main_list[neighbour].predecessor = None

        # Now updating the neighbours
        if main_list[neighbour].partitioning != new_partitioning:
            main_list[neighbour].gain += 2                                              # Changing gain of neighbour
        if main_list[neighbour].partitioning == new_partitioning:
            main_list[neighbour].gain -= 2

        if main_list[neighbour].flipped == False:
            if main_list[neighbour].partitioning == 0:
                move_neigbours(list_0, neighbour)
            else:
                move_neigbours(list_1, neighbour)

    if (main_list[flipped_number].successor is None and                                  # The flipped.nr is on top
        main_list[flipped_number].predecessor is not None):
        list_x[main_list[flipped_number].gain] = main_list[flipped_number].predecessor   # Make the pred the top
        main_list[main_list[flipped_number].predecessor].successor = None                # Update suc of the pred
        main_list[flipped_number].predecessor = None                                     # Resetting pred of flipped.nr

    elif (main_list[flipped_number].predecessor is None and                              # The flipped.nr is below
          main_list[flipped_number].successor is not None):
        main_list[main_list[flipped_number].successor].predecessor = None                # Update pred of the suc
        main_list[flipped_number].successor = None                                       # Resetting suc of flipped.nr

    elif (main_list[flipped_number].predecessor is None and
          main_list[flipped_number].successor is None):
        list_x[main_list[flipped_number].gain] = -1

    else:
        main_list[main_list[flipped_number].successor].predecessor = main_list[flipped_number].predecessor# correct?
        main_list[main_list[flipped_number].predecessor].successor = main_list[flipped_number].successor  # correct?
        main_list[flipped_number].successor = None
        main_list[flipped_number].predecessor = None

    main_list[flipped_number].gain = -1 * main_list[flipped_number].gain                     # Updating gain
    main_list[flipped_number].flipped = True
    return cut_size


def move_neigbours(list_x, neighbour):
    global main_list

    if list_x[main_list[neighbour].gain] != -1:
        main_list[neighbour].predecessor = list_x[main_list[neighbour].gain]
        main_list[list_x[main_list[neighbour].gain]].successor = main_list[neighbour].vertex_number
    list_x[main_list[neighbour].gain] = main_list[neighbour].vertex_number          # putting the neighbour on top


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
    global main_list
    global list_0, list_1
    global pointer_0, pointer_1

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


def reset_main_list():
    global list_0, list_1

    list_0 = {i: -1 for i in range(-30, 31)}
    list_1 = {i: -1 for i in range(-30, 31)}

    numbers = list(range(0, 500))
    random.shuffle(numbers)

    for element in main_list:
        element.flipped = False
        element.successor = None
        element.predecessor = None

    for j in range(0, 500):
        i = numbers[j]
        if main_list[i].partitioning == 0:
            if list_0[main_list[i].gain] == -1:
                list_0[main_list[i].gain] = i
            else:
                previous_number = list_0[main_list[i].gain]
                main_list[previous_number].successor = i
                main_list[i].predecessor = previous_number
                list_0[main_list[i].gain] = i

        else:
            if list_1[main_list[i].gain] == -1:
                list_1[main_list[i].gain] = i
            else:
                previous_number = list_1[main_list[i].gain]
                main_list[previous_number].successor = i
                main_list[i].predecessor = previous_number
                list_1[main_list[i].gain] = i

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




