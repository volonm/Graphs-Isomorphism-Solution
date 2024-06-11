from basicpermutationgroup import Orbit, FindNonTrivialOrbit, Stabilizer, Reduce
from colorref import colorRefine, init_labels_with_degree, computeGroupsOfVertexes
from count_isomorphism import store_graph_snapshot, is_unbalanced, is_bijection, choose_color_class, assign_new_color, \
    restore_graph_from_snapshot
from fastcolorref import fast_colorref
from graph import Vertex, Graph, Edge
from graph_io import load_graph
from newbraching import count_isomorphisms_new
from permv2 import permutation


def simple_generating_set(d_list: list[Vertex], i_list: list[Vertex], g1: Graph, g2: Graph):
    # colorRefine(g1)
    # colorRefine(g2)
    fast_colorref(g1)
    fast_colorref(g2)
    # is_current_subset_known = False
    first_color_group_dict = store_graph_snapshot(g1)
    second_color_group_dict = store_graph_snapshot(g2)

    if is_unbalanced(first_color_group_dict, second_color_group_dict):
        # print("Unbalanced Hit ")
        return 0
    if is_bijection(g1, g2):
        # print("Bijection Hit ")
        is_unique_automorphism(d_list, i_list)
        return 1

    if len(d_list) >= len(g1.vertices):
        return 0
    color_key = choose_color_class(first_color_group_dict)
    d_list, i_list = d_list[:], i_list[:]
    color_group_g_one = first_color_group_dict[color_key]
    color_group_g_two = second_color_group_dict[color_key]
    # sort_vertices_by_id(color_group_g_two)
    vert_x = choose_lowest_by_id(color_group_g_one, d_list, i_list)
    # vert_x = color_group_g_one[0]
    color_group_g_two = sort_by_preference_for_y(color_group_g_two, vert_x)
    assign_new_color(vert_x, g1)
    d_list.append(vert_x)

    snap_shot_g1 = store_graph_snapshot(g1)
    snap_shot_g2 = store_graph_snapshot(g2)

    # print(f"given y list to iter : {get_ids_from_vertices(color_group_g_two)}")
    res = 0
    i_am_main_mapping = True
    if len(d_list) >= 1:
        i_am_main_mapping = get_ids_from_vertices(d_list[:-1]) == get_ids_from_vertices(i_list)
    for i in range(len(color_group_g_two)):
        vert_y = color_group_g_two[i]
        previous_y = find_vertex_alternative(color_group_g_two[i - 1], d_list[:-1], i_list[:-1])
        # Change TO DECIDE THE BACKTRACK RULE
        # if res != 0 and vert_x.id != previous_y.id and not i_am_main_mapping:
        if res != 0 and vert_x.id != previous_y.id:
            # print(f"BACKTRACK DECISION for x - {vert_x.id} | i am main = {i_am_main_mapping}\n {
            # get_ids_from_vertices(color_group_g_two)}") print( f"\nIn this case we return back to main
            # branch\n|d_list|: {get_ids_from_vertices(d_list[:-1])}\n|i_list|: {get_ids_from_vertices(i_list)} ")
            # print( f"Returned to mapping:\n|d_list|: {get_ids_from_vertices(d_list[:-1])}\n|i_list|: {
            # get_ids_from_vertices(i_list)}")
            return 1

        if vert_y in i_list:
            vert_y = find_vertex_alternative(vert_y, d_list[:-1], i_list[:-1])

        # if vert_y and vert_y.id not in get_ids_from_vertices(d_list[:-1]) and not is_current_subset_known:
        if vert_y and vert_y.id not in get_ids_from_vertices(d_list[:-1]):
            i_list.append(vert_y)
            # get_ids_from_vertices(d_list[:-1]) == get_ids_from_vertices(i_list[:-1])
            #
            # if auto_known(d_list, i_list):
            #     i_list.remove(vert_y)
            #     return

            # if not in_need_of_pruning(d_list, i_list):
            vert_y.label = vert_x.label
            res = simple_generating_set(d_list, i_list, g1, g2)
            restore_graph_from_snapshot(snap_shot_g1, snap_shot_g2)
            i_list.remove(vert_y)


def we_need_backtrack(vertex_x: Vertex, vertex_y: Vertex):
    # print(f'd_list: {get_ids_from_vertices(d_list[:-1])} \n| i_list: {get_ids_from_vertices(i_list)}')
    # return get_ids_from_vertices(d_list[:-1]) == get_ids_from_vertices(i_list)
    return vertex_x.id != vertex_y.id
    pass


def auto_known(d_list: list[Vertex], i_list: list[Vertex]):
    cycle = compute_cycle(d_list, i_list)
    permTest = permutation(n=number_of_vertices, cycles=cycle)


def sort_by_preference_for_y(list_vert: list[Vertex], vertex: Vertex):
    res = []
    for vert in list_vert:
        if vert.id == vertex.id:
            res.append(vert)
    for vert in list_vert:
        if vert.id != vertex.id:
            res.append(vert)
    # print(f"sort_by_preference_for_y: vertex_x {vertex.id}\nres = {res}")
    return res


def branch_explored(d_list: list[Vertex], i_list: list[Vertex], y: Vertex):
    orbit_y = Orbit(x_list, y.id)
    if d_list[-1].id == y.id:
        return False
    if get_ids_from_vertices(d_list[:-1]) != get_ids_from_vertices(i_list):
        return len(orbit_y) >= 2
    return False


def order(list_x: list[permutation]):
    # X list:  [(), (1,9), (0,1)(2,9), (41,42)] gives 16 but should 40
    if len(list_x) == 0:
        return 1

    alfa_id = FindNonTrivialOrbit(list_x)
    orbit_of_alfa = Orbit(list_x, alfa_id)

    alfa_stab = Stabilizer(list_x, alfa_id)
    orbit_len = len(orbit_of_alfa)
    # print(
    #     f"id - {alfa_id} , len of orbit {orbit_len} => return res  for alfa stab {alfa_stab} , orbit is {orbit_of_alfa}")

    res = order(alfa_stab) * orbit_len
    return res


def testOrder():
    # test example 1
    rightTR = [[4, 5]]
    leftTR = [[1, 2]]
    flip = [[3, 6], [1, 4], [2, 5]]
    testC = [[3, 6], [1, 5], [2, 4]]
    rightTriangleROtation = permutation(7, rightTR)
    leftTriangleROtation = permutation(7, leftTR)
    flipGraph = permutation(7, cycles=flip)
    # permTotest = permutation(7, testC)
    currentXlist = [rightTriangleROtation, leftTriangleROtation, flipGraph]
    # test example 2

    rightTR = [[0, 1, 2], [4, 5]]
    leftTR = [[2, 3]]
    rightTriangleROtation = permutation(7, rightTR)
    leftTriangleROtation = permutation(7, leftTR)
    currentXlist = [rightTriangleROtation, leftTriangleROtation]
    print(order(currentXlist))
    # print(sifting(currentXlist, permTotest))
    # [(), (1, 9), (0, 1)(2, 9)]

    # test example 3
    rightTR = [[1, 9]]
    # rightTR_2 = [[0, 2]]
    leftTR = [[0, 1], [2, 9]]
    testC = [[41, 42]]

    rightTriangleROtation = permutation(43, rightTR)
    leftTriangleROtation = permutation(43, leftTR)
    # leftTriangleROtation_2 = permutation(72, rightTR_2)
    third_perm = permutation(43, testC)
    currentXlist = [rightTriangleROtation, leftTriangleROtation, third_perm]
    print(currentXlist)
    print(3)
    print(order(currentXlist))
    # print(sifting(currentXlist, permTotest))


def find_position(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


def sifting(list_permutations: list[permutation], perm_to_test: permutation):
    alfa_id = FindNonTrivialOrbit(list_permutations)
    # print(f"alfa_id = {alfa_id} | list_permutations = {list_permutations}, Perem = {perm_to_test}")

    if alfa_id is None:
        return True

    if perm_to_test.istrivial():
        return True

    if len(list_permutations) == 1:
        if list_permutations[0] == perm_to_test:
            return False

    orbit_of_alfa, transversal = Orbit(list_permutations, alfa_id, True)
    image_of_alfa_under_perm = perm_to_test.__getitem__(alfa_id)

    pos = find_position(orbit_of_alfa, image_of_alfa_under_perm)
    if pos == -1:
        return True  # it is unique
    alfa_stab = Stabilizer(list_permutations, alfa_id)
    alfa_transversal_of_mapping = transversal[pos]  # u mapping of betta
    you_betta_inverse = -alfa_transversal_of_mapping
    new_composition = you_betta_inverse * perm_to_test

    return sifting(alfa_stab, new_composition)


def is_unique_automorphism(d_list: list, i_list: list):
    cycle = compute_cycle(d_list, i_list)
    if cycle is None:
        print("To be discussed in this case")
    else:
        perm_to_test = permutation(n=number_of_vertices, cycles=cycle)
        if sifting(x_list, perm_to_test):
            x_list.append(perm_to_test)
            # print(f'X_list has been appended:  {x_list}')
        # else:
            # print(f"Peeee - {perm_to_test} -X has NOT been added ")


def naive_check(permToTest, xlist):  # true if we have it in list
    for perm in xlist:
        if perm == permToTest:
            return True
    return False


# def in_need_of_pruning(d_list: list,
#                        i_list: list) -> bool or None:  # True, if there is need in pruning, False - otherwise.
#     cycle = compute_cycle(d_list, i_list)
#     if cycle is None:
#         return False
#
#     perm_to_test = permutation(n=number_of_vertices, cycles=cycle)
#     # print(f"sifting Descision = {sifting(x_list, perm_to_test)}")
#     if sifting(x_list, perm_to_test):
#         return False
#     return True


def sort_vertices_by_id(vertex_list: list[Vertex]) -> list[Vertex]:
    return sorted(vertex_list, key=lambda vertex: vertex.id)


def choose_lowest_by_id(vertex_list: list[Vertex], d_list: list, i_list: list) -> Vertex:
    vertex_list = sort_vertices_by_id(vertex_list)
    for vert in vertex_list:
        if find_vertex_alternative(vert, d_list, i_list) is not None:
            return find_vertex_alternative(vert, d_list, i_list)


def find_vertex_alternative(vertex: Vertex, d: list, i: list) -> Vertex or None:
    if not vertex_already_mapped(vertex, d, i):
        return vertex
    orbit_of_x = Orbit(x_list, vertex.id)
    if len(orbit_of_x) >= 2:
        for v_id in orbit_of_x:
            # print(f"Comparing ids: {v_id} and {vertex.id}")
            if v_id != vertex.id:
                return find_vertex_by_id(vertex.graph, v_id)
                # return vertex
    return None


def compute_cycle(D_list, I_list):
    res_cycle = []
    for i in range(len(D_list)):
        x_id = D_list[i].id
        y_id = I_list[i].id

        if x_id != y_id:
            cycle = [x_id, y_id]
            res_cycle.append(cycle)
    if len(res_cycle) == 0:
        return res_cycle
    else:
        y_id = res_cycle[-1][1]
        for res in res_cycle[:-1]:
            if res[0] == y_id:
                orbit_of_y = Orbit(x_list, y_id)
                if len(orbit_of_y) >= 2:
                    y_id = orbit_of_y[1]
                else:
                    # print("PROSTO PIZDEC EBLANI!!!!!")
                    return None
        res_cycle[-1][1] = y_id

    # print(f"Generated cycle: {res_cycle} \n| d_list: {D_list} \n| I_list: {I_list}\n| x_list: {x_list} ")
    return res_cycle


def vertex_already_mapped(vertex: Vertex, d_list: list, i_list: list) -> bool:
    for v in d_list:
        if vertex.id == v.id:
            return True
    for v in i_list:
        if vertex.id == v.id:
            return True
    return False


def get_ids_from_vertices(vertices: list[Vertex]) -> list[int]:
    res = []
    for vertex in vertices:
        res.append(vertex.id)
    return res


def find_vertex_by_id(graph: Graph, vertex_id: int) -> Vertex or None:
    for vertex in graph.vertices:
        if vertex.id == vertex_id:
            return vertex
    return None


def calculate_automorphisms(graph):
    init_labels_with_degree(graph)
    colorRefine(graph)
    graph_copy = deep_copy_graph(
        computeGroupsOfVertexes(graph))
    global x_list, number_of_vertices
    x_list = []
    number_of_vertices = len(graph.vertices)

    simple_generating_set([], [], graph, graph_copy)
    # print("After simple_generating_set")

    print(f"X list:  {x_list}")
    # x_list = Reduce(x_list)
    print(f"X list Reduced:  {x_list}")
    return order(x_list)


def deep_copy_graph(color_map: dict) -> Graph:
    if len(color_map) == 0:
        raise WrongGraphError
    highest_id = 0
    vertex_neighbours_map = {}
    is_simple = next(iter(color_map.values()))[0].graph.simple
    is_directed = next(iter(color_map.values()))[0].graph.directed
    graph_copy = Graph(n=0, simple=is_simple, directed=is_directed)
    for key, vertices in color_map.items():
        for vertex in vertices:
            vertex.id = highest_id
            vertex_copy = Vertex(graph_copy)
            vertex_copy.id = highest_id
            vertex_copy.label = key
            vertex_neighbours_map[vertex_copy] = vertex.incidence
            graph_copy.add_vertex(vertex_copy)
            highest_id += 1
    for vertex, edge_list in vertex_neighbours_map.items():
        for edge in edge_list:
            edge_tail_in_copy = find_vertex_by_id(graph_copy, edge.tail.id)
            edge_head_in_copy = find_vertex_by_id(graph_copy, edge.head.id)
            edge_to_add = Edge(edge_tail_in_copy, edge_head_in_copy)
            if check_neighbours_for_copy(vertex, edge_to_add):
                graph_copy.add_edge(edge_to_add)
    return graph_copy


def check_neighbours_for_copy(vertex: Vertex, edge: Edge) -> bool:
    if edge.tail == vertex:
        if edge.head.neighbours.__contains__(vertex):
            return False
    else:
        if edge.tail.neighbours.__contains__(vertex):
            return False
    return True


def generate_all_perm(stabilizer_subgroup):
    n = len(stabilizer_subgroup)
    if n == 0 or n == 1:
        print("HEY")
        return stabilizer_subgroup
    matrix = [[[] for _ in range(n)] for _ in range(n)]
    matrix[0][0] = [stabilizer_subgroup[0] * stabilizer_subgroup[0]]
    for i in range(1, n):
        temp_res_1 = []
        temp_res_2 = []
        for p in matrix[i - 1][0]:
            temp_res_1.append(p * stabilizer_subgroup[i])
            temp_res_1.append(stabilizer_subgroup[i])
        for p in matrix[0][i - 1]:
            temp_res_2.append(p * stabilizer_subgroup[i])
            temp_res_2.append(stabilizer_subgroup[i])
        matrix[i][0] = temp_res_1
        matrix[0][i] = temp_res_2
    for i in range(2, n):
        for j in range(2, n):
            temp_res = [stabilizer_subgroup[j]]
            for perm in matrix[i - 1][j]:
                temp_res.append(perm * stabilizer_subgroup[j])
            for perm in matrix[i][j - 1]:
                temp_res.append(stabilizer_subgroup[j] * perm)
            matrix[i][j] = temp_res
    res = []
    for i in range(n):
        for j in range(n):
            for perm in matrix[i][j]:
                if perm not in res:
                    res.append(perm)

    # print_matrix(matrix)
    # print(f"HEY {matrix[n - 1][n - 1]}")
    # print(f"HEY Res {res}")
    # print(f"HEY Res len {len(res)}")
    return res


def print_matrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])


def example_graph() -> Graph:
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


def book_example():
    test_graph = example_graph()
    num_auto = calculate_automorphisms(test_graph)
    # print("RES")
    # print(x_list)
    print(num_auto)


def test_file():
    # with open("Test/BasicGIAut1.grl") as f:
    #     list_g, _ = load_graph(f=f, read_list=True)
    #     instanceGraph = list_g[2]
    with open("Test/BasicAut1.gr") as f:
        list_g = load_graph(f=f, read_list=False)
        instanceGraph = list_g
    test_graph = instanceGraph
    num_auto = calculate_automorphisms(test_graph)
    print(num_auto)


class WrongGraphError(Exception):
    def __init__(self, message="An empty graph is trying to be copied."):
        self.message = message
        super().__init__(self.message)


if __name__ == '__main__':
    test_file()
    # book_example()
    # testOrder()
    # testOrder()


def useAuto(graph: Graph):
    global x_list, number_of_vertices
    x_list = []
    number_of_vertices = len(graph.vertices)
    graph_copy = initGraphsForAuto(graph)
    simple_generating_set([], [], graph, graph_copy)
    res = order(x_list)
    return res


def initGraphsForAuto(graph: Graph):
    init_labels_with_degree(graph)
    colorRefine(graph)
    graph_copy = deep_copy_graph(
        computeGroupsOfVertexes(graph))
    return graph_copy
