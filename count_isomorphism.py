import time
from typing import List

from colorref import init_labels_with_degree, findPossibleIsomorphisms
from fastcolorref import fast_colorref
from graph import Graph, Vertex, Edge
from graph_io import load_graph, write_dot

global it


def update_unique_vert_lists(d_list: List[Vertex], i_list: List[Vertex], g1_color_map: dict, g2_color_map: dict):
    d_copy = d_list[:]
    i_copy = i_list[:]
    for i in g1_color_map.keys():
        if len(g1_color_map[i]) == 1:
            if not d_list.__contains__(g1_color_map[i][0]):
                d_copy.append(g1_color_map[i][0])
        if g2_color_map.get(i) is not None:
            if len(g2_color_map[i]) == 1:
                if not i_list.__contains__(g2_color_map[i][0]):
                    i_copy.append(g2_color_map[i][0])
    return d_copy, i_copy


def check_single_isomorphism(d_list: list, i_list: list, g1: Graph, g2: Graph) -> int:
    fast_colorref(g1)
    fast_colorref(g2)
    first_color_group_dict = store_graph_snapshot(g1)
    second_color_group_dict = store_graph_snapshot(g2)
    # d_list, i_list = update_unique_vert_lists(d_list, i_list, first_color_group_dict, second_color_group_dict)
    if is_unbalanced_count_iso(first_color_group_dict, second_color_group_dict):
        # print('unbalanced')
        return 0
    if is_bijection(g1, g2):
        print("bij")
        return 1
    if len(d_list) >= len(g1.vertices):
        print('unbalanced')
        return 0
    color_key = choose_color_class(first_color_group_dict)
    # if color_key == -1:
    #     return 0
    color_group_g_one = first_color_group_dict[color_key]
    color_group_g_two = second_color_group_dict[color_key]
    vert_x = color_group_g_one[0]
    d_list.append(vert_x)
    assign_new_color(vert_x, g1)
    snap_shot_g1 = store_graph_snapshot(g1)
    snap_shot_g2 = store_graph_snapshot(g2)
    res = 0
    for vertY in color_group_g_two:
        if res != 0:
            return 1
        if not vertY in i_list:
            vertY.label = vert_x.label
            i_list.append(vertY)
            res = check_single_isomorphism(d_list[:], i_list[:], g1, g2)
            restore_graph_from_snapshot(snap_shot_g1, snap_shot_g2)
            i_list.remove(vertY)

    return res


def check_single_isomorphism_fast_colorref_old(d_list: list, i_list: list, g1: Graph, g2: Graph) -> int:
    # print('count')
    fast_colorref(g1)
    fast_colorref(g2)
    number_of_isomorphism = 0
    first_color_group_dict = store_graph_snapshot(g1)
    second_color_group_dict = store_graph_snapshot(g2)
    # d_list, i_list = update_unique_vert_lists(d_list, i_list, first_color_group_dict, second_color_group_dict)
    if is_unbalanced_count_iso(first_color_group_dict, second_color_group_dict):
        # print("unb")
        return 0
    if is_bijection(g1, g2):
        print("bij")
        return 1
    if len(d_list) >= len(g1.vertices):
        return 0
    color_key = choose_color_class(first_color_group_dict)
    # if color_key == -1:
    #     return 0
    color_group_g_one = first_color_group_dict[color_key]
    color_group_g_two = second_color_group_dict[color_key]
    # vert_x = choose_vertex_x(color_group_g_one, d_list)
    # if vert_x is None:
    #     if len(d_list) == len(g1.vertices):
    #
    #         return 0
    #     choose_vertex_x_printing(color_group_g_one, d_list,i_list)
    vert_x = color_group_g_one[0]
    d_list.append(vert_x)
    assign_new_color(vert_x, g1)
    snap_shot_g1 = store_graph_snapshot(g1)
    snap_shot_g2 = store_graph_snapshot(g2)
    res = 0
    for vertY in color_group_g_two:
        if res != 0:
            return 1
        if not vertY in i_list:
            vertY.label = vert_x.label
            i_list.append(vertY)
            res = check_single_isomorphism_fast_colorref_old(d_list[:], i_list[:], g1, g2)
            restore_graph_from_snapshot(snap_shot_g1, snap_shot_g2)
            i_list.remove(vertY)

    return number_of_isomorphism


def count_isomorphisms(d_list: list, i_list: list, g1: Graph, g2: Graph) -> int:
    # global it
    # print('count')
    fast_colorref(g1)
    fast_colorref(g2)
    number_of_isomorphism = 0
    first_color_group_dict = store_graph_snapshot(g1)
    second_color_group_dict = store_graph_snapshot(g2)
    # d_list, i_list = update_unique_vert_lists(d_list, i_list, first_color_group_dict, second_color_group_dict)
    if is_unbalanced_count_iso(first_color_group_dict, second_color_group_dict):
        # print("unb")
        return 0
    if is_bijection(g1, g2):
        # print("bij")
        # print_single_graph(g1, "g0")
        # print_single_graph(g2, "g1")
        return 1
    # if len(d_list) >= len(g1.vertices):
    #     return 0
    color_key = choose_color_class(first_color_group_dict)
    # if color_key == -1:
    #     return 0

    color_group_g_one = first_color_group_dict[color_key]
    color_group_g_two = second_color_group_dict[color_key]
    # vert_x = choose_vertex_x(color_group_g_one, d_list)
    # if vert_x is None:
    #     if len(d_list) == len(g1.vertices):
    #
    #         return 0
    #     choose_vertex_x_printing(color_group_g_one, d_list,i_list)
    vert_x = color_group_g_one[0]
    d_list.append(vert_x)
    assign_new_color(vert_x, g1)
    snap_shot_g1 = store_graph_snapshot(g1)
    snap_shot_g2 = store_graph_snapshot(g2)
    for vertY in color_group_g_two:
        # if not vertY in i_list:
        vertY.label = vert_x.label
        i_list.append(vertY)
        number_of_isomorphism += count_isomorphisms(d_list[:], i_list[:], g1, g2)
        restore_graph_from_snapshot(snap_shot_g1, snap_shot_g2)
        i_list.remove(vertY)

    return number_of_isomorphism


def choose_vertex_x(vertex_class: list[Vertex], d_vertex: list[Vertex]) -> Vertex or None:
    for vertex in vertex_class:
        if not vertex in d_vertex:
            return vertex
    return None


def choose_vertex_x_printing(vertex_class: list[Vertex], d_vertex: list[Vertex],
                             i_vertex: list[Vertex]) -> Vertex or None:
    print(f"chosen color class {get_labels_from_vertices(vertex_class)}")
    print(f"D list mapped {get_labels_from_vertices(d_vertex)}")
    print(f"I list mapped {get_labels_from_vertices(i_vertex)}")
    for vertex in vertex_class:
        if not vertex in d_vertex:
            return vertex
    return None


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


def choose_color_class(graph_dictionary: dict) -> int:  # Branching rule to choose vertex X.
    # Previous branching Rule
    # lowest_color_key = -1
    # highest_group = -1
    # for key, value in graph_dictionary.items():
    #     if len(value) >= 2:
    #         if highest_group < len(value):
    #             highest_group = len(value)
    #             lowest_color_key = key
    # return lowest_color_key
    lowest_color_key = -1
    lowest_group = 9999999
    for key, value in graph_dictionary.items():
        if len(value) >= 2 and key != 0:
            if lowest_group > len(value):
                lowest_group = len(value)
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


def is_bijection(g1: Graph, g2: Graph):
    # map_1 = store_graph_snapshot(g1)
    # map_2 = store_graph_snapshot(g2)
    # # if not is_balanced(map_1, map_2):
    # #     return False
    vertexes_list_1 = g1.vertices
    vertexes_list_2 = g2.vertices
    labels_list_1 = get_labels_from_vertices(vertexes_list_1)
    labels_list_2 = get_labels_from_vertices(vertexes_list_2)
    is_discrete_graph_1 = len(labels_list_1) == len(set(labels_list_1))
    is_discrete_graph_2 = len(labels_list_2) == len(set(labels_list_2))

    if is_discrete_graph_1 and is_discrete_graph_2:
        for vertex in vertexes_list_1:
            if not check_edges_bijection(vertex, g2):
                return False
        for vertex in vertexes_list_2:
            if not check_edges_bijection(vertex, g1):
                return False
        # print("goes furt")

        return True
    return False


def check_edges_bijection(vertex: Vertex, graph: Graph) -> bool:
    for edge in vertex.incidence:
        head_label = edge.head.label
        tail_label = edge.tail.label
        vertex_in_gr = find_vertex_by_label(graph, vertex.label)
        if len(vertex.neighbours) != len(vertex_in_gr.neighbours):
            return False
        for e in vertex_in_gr.incidence:
            if e.head.label == head_label and e.tail.label == tail_label:
                return True
            if e.head.label == tail_label and e.tail.label == head_label:
                return True
    return False


def is_unbalanced_count_iso(coloring_1: dict, coloring_2: dict) -> bool:
    return not is_balanced_count_iso(coloring_1, coloring_2)


def is_balanced_count_iso(coloring_1: dict, coloring_2: dict) -> bool:
    # if len(coloring_1.keys()) != len(coloring_2.keys()):
    #     return False
    for key, value in coloring_1.items():
        if key not in coloring_2:
            return False
        else:
            if len(value) != len(coloring_2[key]):
                return False
            # for vertex in value:
            #     if not check_edges_bijection(vertex, coloring_2[key][0].graph):
            #         return False
    for key, value in coloring_2.items():
        if key not in coloring_1:
            return False
        else:
            if len(value) != len(coloring_1[key]):
                return False
            # for vertex in value:
            #     if not check_edges_bijection(vertex, coloring_1[key][0].graph):
            #         return False

    return True


def is_unbalanced(coloring_1: dict, coloring_2: dict) -> bool:
    return not is_balanced(coloring_1, coloring_2)


def is_balanced(coloring_1: dict, coloring_2: dict) -> bool:
    if len(coloring_1.keys()) != len(coloring_2.keys()):
        return False
    for key, value in coloring_1.items():
        if key not in coloring_2:
            return False
        else:
            if len(value) != len(coloring_2[key]):
                return False
            # for vertex in value:
            #     if not check_edges_bijection(vertex, coloring_2[key][0].graph):
            #         return False
    for key, value in coloring_2.items():
        if key not in coloring_1:
            return False
        else:
            if len(value) != len(coloring_1[key]):
                return False
            # for vertex in value:
            #     if not check_edges_bijection(vertex, coloring_1[key][0].graph):
            #         return False

    return True


def find_vertex_by_label(g: Graph, label: int) -> Vertex:
    for vertex in g.vertices:
        if vertex.label == label:
            return vertex


# Function which returns dictionary of vertex label as a key and the list of neighbours as a value
def map_vertex_to_neighbours(vertex_list: list) -> dict:
    res = {}
    for vertex in vertex_list:
        if vertex.label not in res:
            res[vertex.label] = get_labels_from_vertices(vertex.neighbours)
    return res


def get_labels_from_vertices(vertices: List[Vertex]) -> List[int]:
    res = []
    for vertex in vertices:
        res.append(vertex.label)
    return sorted(res)


def test(file_name: str, g1_index: int, g2_index: int):
    try:
        with open(f'{file_name}') as file:
            graph_instance_list, options = load_graph(file, read_list=True)
            # print_graph(graph_instance_list, "branching")
            g1 = graph_instance_list[g1_index]
            g2 = graph_instance_list[g2_index]
            print([g1_index, g2_index])
            print(f"len of vertexes - {len(g1.vertices)}")
            init_labels_with_degree(g1)
            init_labels_with_degree(g2)
            start_time = time.time()
            print(count_isomorphisms([], [], g1, g2))
            end_time = time.time()
            print(f"{end_time - start_time}  elapsed time seconds")
    except FileNotFoundError:
        exit(f"File {file_name} not found.")


def test_book_ex():
    # print_graph(graph_instance_list, "branching")
    g1 = example_book_graph()
    g2 = example_book_graph()
    # g1 = graph_instance_list[g1_index]
    # g2 = graph_instance_list[g2_index]
    # print([g1_index, g2_index])
    init_labels_with_degree(g1)
    init_labels_with_degree(g2)
    start_time = time.time()
    print(f"Iso - count {count_isomorphisms([], [], g1, g2)}")
    end_time = time.time()
    print(f"{end_time - start_time}  elapsed time seconds")


def test_instances_list(test_list: list):
    for file_name in test_list:
        print(f"\n\n{file_name}")
        try:
            with open(f'BranchingTestGraphs/{file_name}') as file:
                graph_instance_list, options = load_graph(file, read_list=True)
                graph_dict = {}
                for index, graphInstance in enumerate(graph_instance_list):
                    graph_dict[index] = graphInstance
                    init_labels_with_degree(graphInstance)
                possibly_isomorphic_list = findPossibleIsomorphisms(graph_instance_list)
                print("Sets of isomorphic graphs with automorphisms:")
                for tuple_res in possibly_isomorphic_list:
                    graph_list = tuple_res[0]
                    if len(graph_list) == 2:
                        g1 = graph_dict[graph_list[0]]
                        g2 = graph_dict[graph_list[1]]
                        start_time = time.time()
                        num_isomorphisms = count_isomorphisms([], [], g1, g2)
                        end_time = time.time()
                        duration_single = end_time - start_time
                        print(f"{graph_list} : {num_isomorphisms} -\t {duration_single} ")
                    elif len(graph_list) < 2:
                        print(f"{graph_list}: 0 isomorphic - since 1 graph")
                    else:
                        for i in range(graph_list.length() - 1):
                            g1 = graph_dict[graph_list[i]]
                            for j in range(i + 1, graph_list.length() - 1):
                                g2 = graph_dict[graph_list[j]]
                                start_time = time.time()
                                num_isomorphisms = count_isomorphisms([], [], g1, g2)
                                end_time = time.time()
                                duration_single = end_time - start_time
                                print(f"[{graph_list[i]},{graph_list[j]}] : {num_isomorphisms} -\t {duration_single}")
        except FileNotFoundError:
            exit(f"File {file_name} not found.")


def print_single_graph(graph: Graph, unifier):
    with open(f'testGraph{unifier}.dot', 'w') as file:
        for vertex in graph.vertices:
            vertex.colornum = vertex.label
        write_dot(graph, file)


def example_book_graph() -> Graph:
    graph = Graph(False)
    vert_list = []
    for i in range(7):
        vert = Vertex(graph, i)
        vert_list.append(vert)
        graph.add_vertex(vert)
    zero_edges = []
    for z in range(1, 7):
        z_edge = Edge(vert_list[0], vert_list[z])
        zero_edges.append(z_edge)
        graph.add_edge(z_edge)

    edge13 = Edge(vert_list[1], vert_list[3])
    graph.add_edge(edge13)
    edge32 = Edge(vert_list[3], vert_list[2])
    graph.add_edge(edge32)
    edge46 = Edge(vert_list[4], vert_list[6])
    edge56 = Edge(vert_list[5], vert_list[6])
    graph.add_edge(edge46)
    graph.add_edge(edge56)

    return graph


if __name__ == '__main__':
    test_instances = ["bigtrees1.grl",  # 0
                      "bigtrees2.grl",  # 1
                      "bigtrees3.grl",  # 2
                      "cographs1.grl",  # 3
                      "cubes3.grl",  # 4
                      "cubes4.grl",  # 5
                      "cubes5.grl",  # 6
                      "cubes6.grl",  # 7
                      "cubes7.grl",  # 8
                      "cubes8.grl",  # 9
                      "cubes9.grl",  # 10
                      "modulesC.grl",  # 11
                      "modulesD.grl",  # 12
                      "products72.grl",  # 13
                      "products216.grl",  # 14
                      "regulartwins.grl",  # 15
                      "torus24.grl",  # 16
                      "torus72.grl",  # 17
                      "torus144.grl",  # 18
                      "trees11.grl",  # 19
                      "trees36.grl",  # 20
                      "trees90.grl",  # 21
                      "wheeljoin14.grl",  # 22
                      "wheeljoin25.grl",  # 23
                      "wheeljoin19.grl",  # 24
                      "wheeljoin33.grl",  # 25
                      "wheelstar12.grl",  # 26
                      "wheelstar15.grl",  # 27
                      "wheelstar16.grl"  # 28
                      ]
    small_inst_list = [4, 5, 6, 7, 14, 13, 18, 16, 17, 19, 20, 22, 24, 8]
    # small_inst_list = [24, 8]
    isomorphic_graphs = {4: [[0, 2], [1, 3]], 5: [[0, 2], [1, 3]], 6: [[0, 1], [2, 3]], 7: [[0, 1], [2, 3]],
                         8: [[0, 3], [1, 2]], 16: [[0, 3], [1, 2]], 14: [[0, 6], [1, 7], [2, 9], [3, 8], [4, 5]],
                         13: [[0, 6], [1, 5], [2, 3], [4, 7]], 18: [[0, 6], [1, 7], [2, 4], [3, 10], [5, 9], [8, 11]],
                         17: [[0, 2], [1, 5], [3, 6], [4, 7]], 19: [[0, 3], [1, 4], [2, 5]],
                         20: [[0, 7], [1, 4], [2, 6], [3, 5]], 22: [[0, 1], [2, 3], [4, 7], [5, 6]],
                         24: [[0, 1], [2, 9], [3, 4], [5, 6], [7, 8]]}
    # for file_index in small_inst_list:
    #     start = time.time()
    #     for graph_pair in isomorphic_graphs[file_index]:
    #         print(test_instances[file_index])
    #         test(f"BranchingTestGraphs/{test_instances[file_index]}", graph_pair[0], graph_pair[1])
    #     end = time.time()
    #     duration = end - start
    #     print(f" =======> PASSES FOR EVERY GRAPH | Total {duration} elapsed time seconds |\n\n")

    it = 0
    start = time.time()
    test_book_ex()
    test(f"Test/basicGI2.grl", 0, 1)
    # test(f"BranchingTestGraphs/{test_instances[0]}", 1, 3)
    # test(f"BranchingTestGraphs/{test_instances[24]}", 3, 4)
    # test(f"BranchingTestGraphs/{test_instances[24]}", 5, 6)
    # test(f"BranchingTestGraphs/{test_instances[24]}", 7, 8)
    # print_single_graph()
    # test(f"BranchingTestGraphs/{test_instances[22]}", 7, 8)
    # test(f"BranchingTestGraphs/{test_instances[15]}", 4, 5)

    end = time.time()
    duration = end - start
    print(f" =======> PASSES FOR EVERY GRAPH | Total {duration} elapsed time seconds |")
