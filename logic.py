from copy import deepcopy

from chromosome import Chromosome
from graph_tool.all import *
import random
from Vertex import Vertex
import time

global main_list
global main_list_best, final_main_list
global list_0, list_1
global pointer_0, pointer_1
global gls_list
global fm_passes
global mutation_size



def init(graph_str):
    global main_list, main_list_best
    global final_main_list
    global fm_passes
    global mutation_size
    print("init")
    graph = create_graph_from_str(graph_str)
    smallest_cut_size = 10000000
    fm_passes = 0

    setup_graph(graph)

    # MLS --------------------------------------------------------------
    """
    minimal_cutsize_list = []

    for i in range(0, 5):
        start_time = time.time()
        #print('mls')
        initial_list = setup_initial_list(graph)
        random_partitions = create_random_partitions(initial_list, 2500)
        smallest_cut_size = 100000
        fm_passes = 0

        while fm_passes < 10000:
            main_list = random_partitions.pop()
            fm()
            if fm_passes == 0:
                draw_graph(graph, "two-nodes-color1.pdf")

            final_cut_size = multistart_ls(graph)
            #print(final_cut_size)
            if final_cut_size < smallest_cut_size:
                smallest_cut_size = final_cut_size
                final_main_list = deepcopy(main_list)
            #print(fm_passes)
            #print(smallest_cut_size)

        print(i)
        minimal_cutsize_list.append((smallest_cut_size, time.time() - start_time, final_main_list))

    minimal_cutsize_list.sort(key=lambda x: x[0])
    print("")
    print(f'cut 1: {minimal_cutsize_list[0][0]}, time 1:{minimal_cutsize_list[0][1]}')
    print(f'cut 2: {minimal_cutsize_list[1][0]}, time 2:{minimal_cutsize_list[1][1]}')
    print(f'cut 3: {minimal_cutsize_list[2][0]}, time 3:{minimal_cutsize_list[2][1]}')
    print(f'cut 4: {minimal_cutsize_list[3][0]}, time 4:{minimal_cutsize_list[3][1]}')
    print(f'cut 5: {minimal_cutsize_list[4][0]}, time 5:{minimal_cutsize_list[4][1]}')

    final_main_list = deepcopy(minimal_cutsize_list[0][2])
    new_graph(graph)
    draw_graph(graph, "two-nodes-color2.pdf")
    """
    # MLS --------------------------------------------------------------

    # ILS --------------------------------------------------------------
    """
    mutation_size = 40
    minimal_cutsize_list = []

    print('ils')
    for i in range(0, 5):
        start_time = time.time()
        fm_passes = 0
        smallest_cut_size = 100000
        region_of_attraction = 0

        initial_list = setup_initial_list(graph)
        random_partitions = create_random_partitions(initial_list, 1)
        main_list = random_partitions.pop()
        fm()
        #draw_graph(graph, "two-nodes-color1.pdf")

        smallest_cut_size = multistart_ls(graph)
        final_main_list = deepcopy(main_list)
        while fm_passes < 10000:
            reset_main_list()
            mutate_main_list(smallest_cut_size)
            reset_main_list()
            final_cut_size = multistart_ls(graph)

            #print('')
            #print(smallest_cut_size)
            #print(final_cut_size)
            #print("FM pass # :", fm_passes)

            if final_cut_size == smallest_cut_size:
                region_of_attraction += 1
            if final_cut_size < smallest_cut_size:
                final_main_list = deepcopy(main_list)
                smallest_cut_size = final_cut_size

            else:
                main_list = deepcopy(final_main_list)

        print(i)
        minimal_cutsize_list.append((smallest_cut_size, time.time() - start_time, final_main_list, region_of_attraction))

    minimal_cutsize_list.sort(key=lambda x: x[0])

    print("")
    print(f'cut 1: {minimal_cutsize_list[0][0]}, time 1: {minimal_cutsize_list[0][1]}, attraction: {minimal_cutsize_list[0][3]}')
    print(f'cut 2: {minimal_cutsize_list[1][0]}, time 2: {minimal_cutsize_list[1][1]}, attraction: {minimal_cutsize_list[1][3]}')
    print(f'cut 3: {minimal_cutsize_list[2][0]}, time 3: {minimal_cutsize_list[2][1]}, attraction: {minimal_cutsize_list[2][3]}')
    print(f'cut 4: {minimal_cutsize_list[3][0]}, time 4: {minimal_cutsize_list[3][1]}, attraction: {minimal_cutsize_list[3][3]}')
    print(f'cut 5: {minimal_cutsize_list[4][0]}, time 5: {minimal_cutsize_list[4][1]}, attraction: {minimal_cutsize_list[4][3]}')

    final_main_list = deepcopy(minimal_cutsize_list[0][2])
    new_graph(graph)
    draw_graph(graph, "two-nodes-color2.pdf")

    #final_main_list = deepcopy(main_list)
    #new_graph(graph)
    #draw_graph(graph, "two-nodes-color2.pdf")
    """
    # ILS --------------------------------------------------------------

    # GLS --------------------------------------------------------------
    """
    global gls_list
    minimal_cutsize_list = []

    for i in range(0, 5):                       
        start_time = time.time()
        fm_passes = 0

        gls_list = []
        initial_list = setup_initial_list(graph)
        random_partitions = create_random_partitions(initial_list, 50)
        for partition in random_partitions:
            main_list = partition
            fm()
            cut_size = multistart_ls(graph)
            #print(cut_size)
            gls_list.append([deepcopy(main_list), cut_size])
        gls_list.sort(key=lambda x: x[1])
    
        while fm_passes < 10000:
            #print('gls')                   
            random_nr_1 = random.randint(0, 49)
            random_nr_2 = random.randint(0, 49)
            while random_nr_1 == random_nr_2:
                random_nr_2 = random.randint(0, 49)
            parent_1 = deepcopy(gls_list[random_nr_1][0])
            parent_2 = deepcopy(gls_list[random_nr_2][0])
    
            setup_child(parent_1, parent_2)
    
            cut_size = multistart_ls(graph)
            #print(cut_size)
            #print(fm_passes)
            if cut_size <= gls_list[49][1]:
                gls_list[49] = [deepcopy(main_list), cut_size]
                gls_list.sort(key=lambda x: x[1])
    
        '''for i in gls_list:
            print(i[1])'''

        #final_main_list = deepcopy(gls_list[0][0])
        #print('')
        #print(gls_list[0][1])
    
        minimal_cutsize_list.append((gls_list[0][1], time.time() - start_time, deepcopy(gls_list[0][0])))
        print(i)

    minimal_cutsize_list.sort(key=lambda x: x[0])
    print("")
    print(f'cut 1: {minimal_cutsize_list[0][0]}, time 1:{minimal_cutsize_list[0][1]}')
    print(f'cut 2: {minimal_cutsize_list[1][0]}, time 2:{minimal_cutsize_list[1][1]}')
    print(f'cut 3: {minimal_cutsize_list[2][0]}, time 3:{minimal_cutsize_list[2][1]}')
    print(f'cut 4: {minimal_cutsize_list[3][0]}, time 4:{minimal_cutsize_list[3][1]}')
    print(f'cut 5: {minimal_cutsize_list[4][0]}, time 5:{minimal_cutsize_list[4][1]}')

    final_main_list = deepcopy(minimal_cutsize_list[0][2])
    new_graph(graph)
    draw_graph(graph, "two-nodes-color2.pdf")
    """
    # GLS --------------------------------------------------------------

    return Graph()


def draw_graph(graph, string):
    graph_draw(
        graph,
        vertex_text=graph.vertex_index,
        vertex_fill_color=graph.vertex_properties["color"],
        output=string)


# this is 0-based indexing, thus (textfile_index - 1).
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


def fm():
    #print("fm")
    # partition graph (not the arrays)
    #a, b = partition(graph)

    # print(len(a))
    # print(len(b))

    setup()

    # compute gains
    # gain = v.neighbors in B (A) - v.neighbors in A (B)


def setup_graph(graph):
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

def setup_initial_list(graph):
    # Here I set up the entire main_list meaning I determine:
    # vertex number
    # partitioning (0 or 1)
    # gain
    # connected vertex
    # predecessor
    # successor

    initial_list = []
    for i in range(0, 500):
        if graph.vertex_properties["color"][graph.vertex(i)] == "#1c71d8":
            initial_list.append(Vertex(i, 0, [int(n) for n in graph.vertex(i).all_neighbors()]))
        if graph.vertex_properties["color"][graph.vertex(i)] == "#2ec27e":
            initial_list.append(Vertex(i, 1, [int(n) for n in graph.vertex(i).all_neighbors()]))
    return initial_list

def create_random_partitions(initial_list, total_partitions):
    total_vertices = len(initial_list)
    partition_size = total_vertices // 2
    partitions = []

    # create 2500 random initial partitions
    for _ in range(total_partitions):
        current_partition = deepcopy(initial_list)
        a = random.sample(range(total_vertices), partition_size)
        b = [i for i in range(total_vertices) if i not in a]
        # partition each random initial partition
        for i in a:
            current_partition[i].partitioning = 0
        for i in b:
            current_partition[i].partitioning = 1
        partitions.append(current_partition)
    return partitions


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
    global main_list, main_list_best
    global list_0, list_1
    global pointer_0, pointer_1
    mutation_bool = False
    global fm_passes

    cut_size = 0
    lowest_cut_size = 1000000000
    cut_size_lowered = True

    # finding current cut size
    for edge in graph.edges():
        a, b = edge
        if main_list[int(a)].partitioning != main_list[int(b)].partitioning:
            cut_size += 1

    while cut_size_lowered:
        cut_size_lowered = False
        for i in range(0, 500):
            if i % 2 == 0:                                                                  # Flipping 0,1,0,1..
                for j in reversed(range(-16, 17)):
                    if list_0[j] != -1:
                        pointer_0 = j
                        break
                new_cut_size = update_list(1, list_0, pointer_0, cut_size, mutation_bool, 0)
                cut_size = new_cut_size

            else:
                for j in reversed(range(-16, 17)):
                    if list_1[j] != -1:
                        pointer_1 = j
                        break
                new_cut_size = update_list(0, list_1, pointer_1, cut_size, mutation_bool, 0)
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

        fm_passes += 1

    #test = 0
    #print(main_list)
    #print(lowest_cut_size)
    #print(cut_size)
    #for element in main_list:
        #if element.partitioning ==1:
            #test += 1
    #print(test)

    return cut_size


def mutate_main_list(cut_size):
    global main_list, main_list_best
    global list_0, list_1
    global pointer_0, pointer_1
    global mutation_size
    mutation_bool = True

    list_zeros = []
    list_ones = []

    for element in main_list:
        if element.partitioning == 0:
            list_zeros.append(element.vertex_number)
        if element.partitioning == 1:
            list_ones.append(element.vertex_number)

    for i in range(0, mutation_size):     # Needs to always be divisible by 2! Not specified in assignment how high it should be, ToDo: find the sweetspot?
        if i % 2 == 0:                                      # Flipping 0,1,0,1..
            random.shuffle(list_zeros)
            mutation_spot = list_zeros[0]
            list_zeros.remove(mutation_spot)
            cut_size = update_list(1, list_0, pointer_0, cut_size, mutation_bool, mutation_spot)
        else:
            random.shuffle(list_ones)
            mutation_spot = list_ones[0]
            list_ones.remove(mutation_spot)
            cut_size = update_list(0, list_1, pointer_1, cut_size, mutation_bool, mutation_spot)

    return cut_size


def update_list(new_partitioning, list_x, pointer, cut_size, mutation_bool, mutation_spot):
    global main_list
    global list_0, list_1

    if mutation_bool:
        flipped_number = mutation_spot
    else:
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

    #print(main_list[neighbour].vertex_number)
    #print(main_list[neighbour].gain)
    #print()
    if list_x[main_list[neighbour].gain] != -1:
        main_list[neighbour].predecessor = list_x[main_list[neighbour].gain]
        main_list[list_x[main_list[neighbour].gain]].successor = main_list[neighbour].vertex_number
    list_x[main_list[neighbour].gain] = main_list[neighbour].vertex_number          # putting the neighbour on top


def iterated_ls(main_list, list_0, list_1, pointer_0, pointer_1):
    print("ils")


def genetic_ls(main_list, list_0, list_1, pointer_0, pointer_1):
    print("gls")




def setup_child(parent_1, parent_2):
    global main_list

    main_list = deepcopy(parent_1)
    difference_list = []
    hamming_distance = 0

    for i in range(0, 500):
        if parent_1[i].partitioning != parent_2[i].partitioning:
            hamming_distance += 1
    if hamming_distance > 250:
        for i in range(500):
            parent_2[i].partitioning = 1 - parent_2[i].partitioning

    list_01 = []
    zeros = 0
    for i in range(0, 500):
        if parent_1[i].partitioning != parent_2[i].partitioning:
            difference_list.append(i)
        else:
            if parent_1[i].partitioning == 0:
                zeros += 1
    for i in range(250 - zeros):
        list_01.append(0)
    for i in range(250 - (500 - len(difference_list) - zeros)):
        list_01.append(1)
    random.shuffle(list_01)
# ToDo: can/should we do this faster?

    for i in range(len(difference_list)):
        main_list[difference_list[i]] = Vertex(difference_list[i], list_01[i], [int(n) for n in parent_1[difference_list[i]].connected_vertexes])

    setup()



def setup():
    global main_list
    global list_0, list_1
    global pointer_0, pointer_1

    list_0 = {i: -1 for i in range(-16, 17)}
    list_1 = {i: -1 for i in range(-16, 17)}

    numbers = list(range(0, 500))
    random.shuffle(numbers)

    for element in main_list:
        element.flipped = False
        element.successor = None
        element.predecessor = None

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

def reset_main_list():
    global list_0, list_1

    list_0 = {i: -1 for i in range(-16, 17)}
    list_1 = {i: -1 for i in range(-16, 17)}

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




