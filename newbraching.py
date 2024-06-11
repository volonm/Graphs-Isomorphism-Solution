from colorref import colorRefine
from count_isomorphism import is_unbalanced_count_iso, is_bijection, choose_color_class, assign_new_color, \
    store_graph_snapshot, print_single_graph
from fastcolorref import fast_colorref
from graph import Graph, Vertex


def resetGraph(g1):
    for vert in g1.vertices:
        if vert.degree != 0:
            vert.label = 1


def setLabels(d_list: list[Vertex], i_list: list[Vertex], g1: Graph, g2: Graph):
    resetGraph(g1)
    resetGraph(g2)
    for vertid in range(len(d_list)):
        vertX = d_list[vertid]
        assign_new_color(vertX, g1)
        vertY = i_list[vertid]
        vertY.label = vertX.label


def count_isomorphisms_new(d_list: list, i_list: list, g1: Graph, g2: Graph) -> int:
    setLabels(d_list, i_list, g1, g2)
    colorRefine(g1)
    colorRefine(g2)
    number_of_isomorphism = 0
    first_color_group_dict = store_graph_snapshot(g1)
    second_color_group_dict = store_graph_snapshot(g2)

    if is_unbalanced_count_iso(first_color_group_dict, second_color_group_dict):
        return 0
    if is_bijection(g1, g2):
        return 1
    if len(d_list) >= len(g1.vertices):
        return 0
    color_key = choose_color_class(first_color_group_dict)
    if color_key == -1:
        return 0
    color_group_g_one = first_color_group_dict[color_key]
    color_group_g_two = second_color_group_dict[color_key]
    vert_x = color_group_g_one[0]
    d_list.append(vert_x)
    assign_new_color(vert_x, g1)
    for vertY in color_group_g_two:
        vertY.label = vert_x.label
        i_list.append(vertY)
        number_of_isomorphism += count_isomorphisms_new(d_list[:], i_list[:], g1, g2)
        i_list.remove(vertY)

    return number_of_isomorphism


def check_single_isomorphism_fast_colorref(d_list: list, i_list: list, g1: Graph, g2: Graph) -> int:
    setLabels(d_list, i_list, g1, g2)
    # colorRefine(g1)
    # colorRefine(g2)
    fast_colorref(g1)
    fast_colorref(g2)
    number_of_isomorphism = 0
    first_color_group_dict = store_graph_snapshot(g1)
    second_color_group_dict = store_graph_snapshot(g2)

    if is_unbalanced_count_iso(first_color_group_dict, second_color_group_dict):
        print("unb")
        return 0
    if is_bijection(g1, g2):
        print("bij")
        return 1
    if len(d_list) >= len(g1.vertices):
        return 0
    color_key = choose_color_class(first_color_group_dict)
    if color_key == -1:
        return 0
    color_group_g_one = first_color_group_dict[color_key]
    color_group_g_two = second_color_group_dict[color_key]
    vert_x = color_group_g_one[0]
    d_list.append(vert_x)
    assign_new_color(vert_x, g1)
    for vertY in color_group_g_two:
        if number_of_isomorphism == 1:
            return 1
        vertY.label = vert_x.label
        i_list.append(vertY)
        number_of_isomorphism = check_single_isomorphism_fast_colorref(d_list[:], i_list[:], g1, g2)
        i_list.remove(vertY)

    return number_of_isomorphism

