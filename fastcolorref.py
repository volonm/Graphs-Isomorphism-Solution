import time
from collections import defaultdict

from graph import Graph
from graph_io import load_graph, write_dot


def degree_coloring(graph: Graph):
    degrees = []
    color_classes = defaultdict(list)
    for vert in graph.vertices:
        # vert.label = vert.degree
        if vert.label not in degrees:
            degrees.append(vert.label)
        color_classes[vert.label].append(vert)
    return degrees, color_classes


# L - лист цветов i, которые соединены с цветом C ([1])
# A[1] - количество верщин цвета 1 соединённых с цветом C (5)
# A[2] = 1, A[3] = 2
# loop over L:
#    изменить цвет i если A[i] < количество верщин цвета i в графе (A[1] = 5, всего зелёных 6, значит split зелёный цвет)
#    остальные вершины цвета i которые не соединены с С оставить того же цвета
#    добавить в очередь либо новый цвет, либо старый, в зависимости от того, где меньше вершин
# удаляем цвет С из очереди, повторяем алгоритм для следующего в очереди
# если очередь пустая -> закончить

def uniform_coloring(graph: Graph):
    for vert in graph.vertices:
        vert.label = 0
    return graph


def L(neighbours: list):
    L_dict = defaultdict(list)
    for vert in neighbours:
        L_dict[vert.label].append(vert)
        '''
                if vert.label in L_dict.keys():
                    L_dict[vert.label].append(vert)
                else:
                    L_dict[vert.label] = [vert]'''
    return L_dict


def maxcolor(graph: Graph):
    max_color = 0
    for vert in graph.vertices:
        max_color = max(max_color, vert.label)
    return max_color


def change_color(graph: Graph, change: set, leave: set, color_dict: defaultdict, color: int):
    new_color = maxcolor(graph) + 1
    for vert in change:
        vert.label = new_color
    color_dict[color], color_dict[new_color] = list(leave), list(change)
    return new_color, color_dict


def split_color(graph: Graph, L_list: dict, quue: list, dur_inl, dur_change, color_dict: dict):
    sorted_keys = sorted(L_list.keys())
    for color in sorted_keys:
        color_class = set(color_dict[color])
        if len(L_list[color]) < len(color_class):
            start_inl = time.time()
            not_in_l = color_class - set(L_list[color])
            in_l = color_class.intersection(L_list[color])
            dur_inl += time.time() - start_inl
            if len(in_l) < len(not_in_l):
                start_change = time.time()
                new_color, color_dict = change_color(graph, in_l, not_in_l, color_dict, color)
                dur_change += time.time() - start_change
            else:
                start_change = time.time()
                new_color, color_dict = change_color(graph, not_in_l, in_l, color_dict, color)
                dur_change += time.time() - start_change
            quue.append(new_color)
    return quue, dur_inl, dur_change, color_dict


def i_neighbours(graph: Graph, C: int, C_vert: list):
    i = defaultdict(list)
    count = {}
    for vert in C_vert:
        for neigh in vert.neighbours:
            if neigh in count:
                i[count[neigh]].remove(neigh)
                count[neigh] += 1
                i[count[neigh]].append(neigh)
            else:
                count[neigh] = 1
                i[1].append(neigh)
    return i


def fast_colorref(graph: Graph):
    dur_vert, dur_inl, dur_change, dur_split, dur_L, dur_i = 0, 0, 0, 0, 0, 0
    start = time.time()
    quue, color_classes = degree_coloring(graph)
    quue = sorted(quue)[:-1]
    while quue:
        start_i = time.time()
        i = i_neighbours(graph, quue[0], color_classes[quue[0]])
        dur_i += time.time() - start_i
        for num in sorted(i.keys()):
            start_L = time.time()
            L_list = L(i[num])
            dur_L += time.time() - start_L
            start_split = time.time()
            quue, dur_inl, dur_change, color_classes = split_color(graph, L_list, quue, dur_inl,
                                                                   dur_change, color_classes)
            dur_split += time.time() - start_split
        quue.pop(0)
    dur_ref = time.time() - start
    # print(f"ref {dur_ref}, 100%")
    # print(f"split {dur_split}, {dur_split * 100 / dur_ref}%")
    # print(f"L {dur_L}, {dur_L * 100 / dur_ref}%")
    # print(f"inl {dur_inl}, {dur_inl * 100 / dur_ref}%")
    # print(f"change {dur_change}, {dur_change * 100 / dur_ref}%")
    # print((f"i {dur_i}, {dur_i * 100 / dur_ref}%"))
    return graph


def open_fastcolorref(filePath):
    with open(filePath) as file:
        graphInstanceList, options = load_graph(file, read_list=True)
        for graphInstance in graphInstanceList:
            fast_colorref(graphInstance)
        return graphInstanceList


def print_graph(graph_list: list[Graph], filepath: str):
    for i in range(len(graph_list)):
        graph = graph_list[i]
        with open(f'{filepath}{i}.dot', 'w') as file:
            for vertex in graph.vertices:
                vertex.colornum = vertex.label
            write_dot(graph, file)
            print(1)


# test_list = [
#     "colorref_largeexample_4_1026.grl",
#     "colorref_largeexample_6_960.grl",
#     "colorref_smallexample_2_49.grl",
#     "colorref_smallexample_4_16.grl",
#     "colorref_smallexample_4_7.grl",
#     "colorref_smallexample_6_15.grl",
#     "cref9vert3comp_10_27.grl",
#     "test_3reg.grl",
#     "test_cref9.grl",
#     "test_cycles.grl",
#     "test_empty.grl",
#     "test_iter.grl",
#     "test_trees.grl",
# ]

test_list = [
    "threepaths5.gr",
    "threepaths10.gr",
    "threepaths20.gr",
    "threepaths40.gr",
    "threepaths80.gr",
    "threepaths160.gr",
    "threepaths320.gr",
    "threepaths640.gr",
    "threepaths1280.gr",
    "threepaths2560.gr",
    "threepaths5120.gr",
    "threepaths10240.gr",

]


def assign_vertex_by_degree(graph: Graph):
    for vertex in graph.vertices:
        vertex.label = vertex.degree


def group_graphs_by_iso(path):
    try:
        with open(path) as f:
            print(f"{path}")
            G, properties = load_graph(f, Graph, read_list=True)

        graph_dict = {}
        colors_graphs = {}
        graph_iteration = {}
        start = time.time()
        for index, file_graph in enumerate(G):
            assign_vertex_by_degree(file_graph)
            fast_colorref(file_graph)
            iteration = 0
            graph_dict[index] = file_graph
            graph_iteration[index] = iteration
        duration = time.time() - start
        # print_graph(G, "test")
        print(f"Partitioning of the file took ---> Total {duration} elapsed time seconds |")
        separate_groups = {}
        # For each graph in the given file
        for graph_index, value in graph_dict.items():
            colors = tuple(get_all_colors(graph_dict.get(graph_index)))
            # print(f"{graph_index} + \t {colors}")
            same_links = False
            if colors in colors_graphs.keys():
                graphs = colors_graphs[colors]
                if are_perfectly_edged(graph_dict[graphs[0]].edges, graph_dict[graph_index].edges):
                    same_links = True
                # for gr_index in graphs:
                #     # print(f"Comparing {graph_index} and {gr_index}")
                #     if are_perfectly_edged(graph_dict[gr_index].edges, graph_dict[graph_index].edges):
                #         same_links = True
                if same_links:
                    colors_graphs[colors].append(graph_index)
                else:
                    separate_groups[len(separate_groups)] = graph_index
            else:
                colors_graphs[colors] = [graph_index]

        res = []
        for colors, group in colors_graphs.items():
            discrete = len(colors) == len(set(colors))
            iteration = graph_iteration[group[0]]
            res.append((group, iteration, discrete))

        # check and add the separate graph groups
        if len(separate_groups.keys()) == 1:
            separate_groups_keys = list(separate_groups.keys())
            g_index = separate_groups[separate_groups_keys[0]]
            discrete = len(get_all_colors(graph_dict[g_index])) == len(set(get_all_colors(graph_dict[g_index])))
            res.append(([g_index], graph_iteration[g_index], discrete))
        elif len(separate_groups.keys()) > 1:
            for g1 in separate_groups.values():
                temporary_group = [g1]
                for g2 in separate_groups.values():
                    if (g1 != g2) and are_perfectly_edged(graph_dict[g1].edges, graph_dict[g2].edges):
                        temporary_group.append(g2)
                if len(temporary_group) > 0:
                    vertexes = get_all_colors(graph_dict[g1])
                    discrete = len(vertexes) == len(set(vertexes))
                    temporary_group = list(sorted(set(temporary_group)))
                    tuple_group_res = (temporary_group, graph_iteration[temporary_group[0]], discrete)
                    if tuple_group_res not in res:
                        res.append(tuple_group_res)

        # Printing the results
        print("Sets of possibly isomorphic graphs:")
        for tuple_res in res:
            if tuple_res[2]:
                print(f"{tuple_res[0]} {tuple_res[1]} discrete")
            else:
                print(f"{tuple_res[0]}  {tuple_res[1]}")
        print("\n")
        return graph_dict, res
    except FileNotFoundError:
        exit("File not found.")


def are_perfectly_edged(edges: list, edges1: list):
    if len(edges) != len(edges1):
        return False
    else:
        dict_edges = edges_to_dict(edges)
        dict_edges2 = edges_to_dict(edges1)
        for key in dict_edges:
            if key not in dict_edges2:
                return False
            if dict_edges[key] != dict_edges2[key]:
                return False
    return True


def get_all_colors(g: Graph) -> list:
    res = []
    for vertex in g.vertices:
        res.append(vertex.label)
    return sorted(res)


def edges_to_dict(edges: list) -> dict:
    dict_edges = {}
    for edge in edges:
        if edge.head.label < edge.tail.label:
            edge_to_store = tuple([edge.head.label, edge.tail.label])
        else:
            edge_to_store = tuple([edge.tail.label, edge.head.label])

        if edge_to_store not in dict_edges:
            dict_edges[edge_to_store] = 1
        else:
            dict_edges[edge_to_store] = dict_edges[edge_to_store] + 1

    return dict_edges


def f():
    for instance in test_list:
        group_graphs_by_iso(f"SampleGraphsBasicColorRefinement/{instance}")


# if __name__ == '__main__':
#     for instance in test_list:
#         group_graphs_by_iso(f"SampleGraphsBasicColorRefinement/{instance}")
# cProfile('f()')

if __name__ == '__main__':
    group_graphs_by_iso("Test/basicGI1.grl")
    # for instance in test_list:
    #     group_graphs_by_iso(f"SampleGraphsFastColorRefinement/{instance}")
