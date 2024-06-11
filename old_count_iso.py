import time

from graph import Graph, Vertex
from colorref import colorRefine, init_labels_with_degree, findPossibleIsomorphisms
from graph_io import load_graph


def count_isomorphisms(g1: Graph, g2: Graph) -> int:
    colorRefine(g1)
    colorRefine(g2)
    number_of_isomorphism = 0
    first_color_group_dict = store_graph_snapshot(g1)
    second_color_group_dict = store_graph_snapshot(g2)
    if is_unbalanced(g1, g2):
        return 0
    if is_bijection(g1, g2):
        return 1
    color_key = choose_color_class(first_color_group_dict)
    color_group_g_one = first_color_group_dict[color_key]
    color_group_g_two = second_color_group_dict[color_key]
    vert_x = color_group_g_one[0]
    assign_new_color(vert_x, g1)
    snap_shot_g1 = store_graph_snapshot(g1)
    snap_shot_g2 = store_graph_snapshot(g2)
    for vertY in color_group_g_two:
        vertY.label = vert_x.label
        number_of_isomorphism += count_isomorphisms(g1, g2)
        restore_graph_from_snapshot(snap_shot_g1, snap_shot_g2)
    return number_of_isomorphism


def restore_graph_from_snapshot(snapShotG1, snapShotG2):  # restores graph to snapshot state
    for color_class, vertex_list in snapShotG1.items():
        for vertex in vertex_list:
            vertex.label = color_class
    for color_class, vertex_list in snapShotG2.items():
        for vertex in vertex_list:
            vertex.label = color_class


def assign_new_color(vert_X: Vertex, graph: Graph):  # returns new highest color int
    vertexes = graph.vertices
    max_color = -1
    for vertex in vertexes:
        if vertex.label > max_color:
            max_color = vertex.label
    vert_X.label = max_color + 1


def choose_color_class(graph_dictionary: dict) -> int:  # returns a key to smallest color class with 2 elements or more
    lowest_color_key = -1
    highest_group = -1
    for key, value in graph_dictionary.items():
        if len(value) >= 2:
            if highest_group < len(value):
                highest_group = len(value)
                lowest_color_key = key
    return lowest_color_key


def store_graph_snapshot(graph: Graph) -> dict:  # makes a dictionary with color key and array of vertexes
    res = {}
    for vertex in graph.vertices:
        if vertex.label not in res:
            res[vertex.label] = [vertex]
        else:
            res[vertex.label].append(vertex)
    return res


# To choose
def is_unbalanced(g1: Graph, g2: Graph) -> bool:
    g1_label_list = [vertex.label for vertex in g1.vertices]
    g2_label_list = [vertex.label for vertex in g2.vertices]
    g1_label_list.sort()
    g2_label_list.sort()
    g1_label_tuple = tuple(g1_label_list)
    g2_label_tuple = tuple(g2_label_list)
    if g1_label_tuple == g2_label_tuple:
        return False
    else:
        return True


def is_bijection(g1: Graph, g2: Graph) -> bool:
    # The bijection happens when the graphs are discrete, len of their vertexes is same and each vertex has the same
    # neighbour.
    vertexes_list_1 = g1.vertices
    vertexes_list_2 = g2.vertices
    labels_list_1 = get_labels_from_vertices(vertexes_list_1)
    labels_list_2 = get_labels_from_vertices(vertexes_list_2)
    is_discrete_graph_1 = len(labels_list_1) == len(set(labels_list_1))
    is_discrete_graph_2 = len(labels_list_2) == len(set(labels_list_2))
    same_number_vertex = len(vertexes_list_1) == len(vertexes_list_2)
    same_len_vertex = len(labels_list_1) == len(labels_list_2)
    if same_len_vertex and same_number_vertex and is_discrete_graph_1 and is_discrete_graph_2:
        # A bijection f : V (G) → V (H) follows D, I, if for all i ∈ {1, ., ., ., d}: f (xi) = yi
        # Seems that there is no need to check. However, to be tested on all instances
        # dictionary_of_neighbours_1 = map_vertex_to_neighbours(vertexes_list_1)
        # dictionary_of_neighbours_2 = map_vertex_to_neighbours(vertexes_list_2)
        # for key, value in dictionary_of_neighbours_1.items():
        #     if key not in dictionary_of_neighbours_2:
        #         return False
        #     if value != dictionary_of_neighbours_2[key]:
        #         return False
        return True
    return False


# Function which returns dictionary of vertex label as a key and the list of neighbours as a value
def map_vertex_to_neighbours(vertex_list: list) -> dict:
    res = {}
    for vertex in vertex_list:
        if vertex.label not in res:
            res[vertex.label] = get_labels_from_vertices(vertex.neighbours)
    return res


def get_labels_from_vertices(vertices: list) -> list:
    res = []
    for vertex in vertices:
        res.append(vertex.label)
    return sorted(res)


def test(file_name: str, g1_index: int, g2_index: int):
    try:
        with open(f'BranchingTestGraphs/{file_name}') as file:
            graphInstanceList, options = load_graph(file, read_list=True)
            g1 = graphInstanceList[g1_index]
            g2 = graphInstanceList[g2_index]
            print(f"g1 : {len(g1.vertices)}")
            print(f"g2 : {len(g2.vertices)}")
            init_labels_with_degree(g1)
            init_labels_with_degree(g2)
            start = time.time()
            print(count_isomorphisms(g1, g2))
            end = time.time()
            print(f"{end - start}  elapsed time seconds")
    except FileNotFoundError:
        exit(f"File {file_name} not found.")


def test_instances_list(test_list: list):
    for file_name in test_list:
        print(f"\n\n{file_name}")
        try:
            with open(f'BranchingTestGraphs/{file_name}') as file:
                graphInstanceList, options = load_graph(file, read_list=True)
                graph_dict = {}
                for index, graphInstance in enumerate(graphInstanceList):
                    graph_dict[index] = graphInstance
                    init_labels_with_degree(graphInstance)
                possibly_isomorphic_list = findPossibleIsomorphisms(graphInstanceList)
                print("Sets of isomorphic graphs with automorphisms:")
                for tuple_res in possibly_isomorphic_list:
                    graph_list = tuple_res[0]
                    if len(graph_list) == 2:
                        g1 = graph_dict[graph_list[0]]
                        g2 = graph_dict[graph_list[1]]
                        start = time.time()
                        num_isomorphisms = count_isomorphisms(g1, g2)
                        end = time.time()
                        duration = end - start
                        print(f"{graph_list} : {num_isomorphisms} -\t {duration} ")
                    elif len(graph_list) < 2:
                        print(f"{graph_list}: 0 isomorphic - since 1 graph")
                    else:
                        for i in range(graph_list.length() - 1):
                            g1 = graph_dict[graph_list[i]]
                            for j in range(i + 1, graph_list.length() - 1):
                                g2 = graph_dict[graph_list[j]]
                                start = time.time()
                                num_isomorphisms = count_isomorphisms(g1, g2)
                                end = time.time()
                                duration = end - start
                                print(f"[{graph_list[i]},{graph_list[j]}] : {num_isomorphisms} -\t {duration}")
        except FileNotFoundError:
            exit(f"File {file_name} not found.")


if __name__ == '__main__':
    test_instances = ["bigtrees1.grl",
                      "bigtrees2.grl",
                      "bigtrees3.grl",
                      "cographs1.grl",
                      "cubes3.grl",
                      "cubes4.grl",
                      "cubes5.grl",
                      "cubes6.grl",
                      "cubes7.grl",
                      "cubes8.grl",
                      "cubes9.grl",
                      "modulesC.grl",
                      "modulesD.grl",
                      "products72.grl",
                      "products216.grl",
                      "regulartwins.grl",
                      "torus24.grl",
                      "torus72.grl",
                      "torus144.grl",
                      "trees11.grl",
                      "trees36.grl",
                      "trees90.grl",
                      "wheeljoin14.grl",
                      "wheeljoin25.grl",
                      "wheeljoin33.grl",
                      "wheeljoin33.grl",
                      "wheelstar12.grl",
                      "wheelstar15.grl",
                      "wheelstar16.grl"
                      ]
    # test_instances_list(test_instances)
    # test(test_instances[7], 2, 3)
    print(test_instances[12])
    test(test_instances[12], 0, 2)

