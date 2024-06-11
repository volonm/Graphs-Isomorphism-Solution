import time

from colorref import computeGroupsOfVertexes, init_labels_with_degree
from count_auto_final import deep_copy_graph, useAuto, initGraphsForAuto
from count_isomorphism import count_isomorphisms, print_single_graph, check_single_isomorphism_fast_colorref_old, \
    check_single_isomorphism
from fastcolorref import group_graphs_by_iso, fast_colorref
from graph import Graph
from graph_io import load_graph
from newbraching import count_isomorphisms_new, check_single_isomorphism_fast_colorref


def run_test():
    with open("Test/basicAut1.gr") as f:
        list_g = load_graph(f)
        g1 = list_g

        # g2 = list_g[2]
    #

    print(len(g1.vertices))

    init_labels_with_degree(g1)
    # init_labels_with_degree(g2)
    # colorRefine(g1)
    # colorRefine(g2)

    #
    graph_copy = deep_copy_graph(
        computeGroupsOfVertexes(g1))
    print("we")
    start = time.time()
    res = count_isomorphisms([], [], g1, graph_copy)
    end = time.time()

    print(res)
    print(f"{end - start}  elapsed time seconds")


# Sets of isomorphic graphs:
# First Refinement
# [0, 6, 4, 7]
# [1,2]


# [0, 6]
# [1, 5]
def solve_graph_isomorphisms(file_path: str):
    print(f"{file_path}:")
    graph_dict, first_refinement = group_graphs_by_iso(file_path)
    partition_dict = []
    for tuple_res in first_refinement:
        possibly_isomorphic_graphs = tuple_res[0]
        new_partition_list = []
        i = 0
        while i < len(possibly_isomorphic_graphs):
            g1_index = possibly_isomorphic_graphs[i]
            isomorphic_with_g1 = [g1_index]
            for j in range(len(possibly_isomorphic_graphs)):
                g2_index = possibly_isomorphic_graphs[j]
                if g1_index != g2_index:
                    g1 = graph_dict[g1_index]
                    g2 = graph_dict[g2_index]
                    # if check_single_isomorphism_fast_colorref([],[],g1,g2):
                    # init_labels_with_degree(g1)
                    # init_labels_with_degree(g2)
                    # fast_colorref(g1)
                    # fast_colorref(g2)
                    # print_single_graph(g1, "LALA")
                    # print_single_graph(g2, "LALA2")
                    print(f"Check graphs {g1_index} and {g2_index}")
                    if check_single_isomorphism_fast_colorref([], [], g1, g2) > 0:
                        print(f"Iso graphs {g1_index} and {g2_index}")
                        isomorphic_with_g1.append(g2_index)
                    print("WE CHECKED AKFGJASDLGHA")
            for e in isomorphic_with_g1:
                possibly_isomorphic_graphs.remove(e)
            i += 1
            new_partition_list.append(sorted(isomorphic_with_g1))
        # eliminate copies
        for i in range(len(new_partition_list)):
            for j in range(len(new_partition_list)):
                if i != j and new_partition_list[i] == new_partition_list[j]:
                    new_partition_list.remove(new_partition_list[j])

        # add tuple's new partition to dictionary
        partition_dict.append(new_partition_list)
    print("Equivalence classes:")
    for partition in partition_dict:
        print(partition)


# Graph: Number of automorphisms:
# 0: 288
# 1: 576
def solve_graph_automorphisms(graph_list: list[Graph], mode):  # if mode true run them as auto
    print("Graph: Number of automorphisms:")
    i = 0;
    start = time.time()
    for graph in graph_list:

        if mode:
            res = useAuto(graph)
        else:
            res = useIso(graph)

        print(f"Graph {i} :{res}")
        i += 1
    end = time.time()
    print(f"{end - start}  elapsed time seconds")


def useIso(graph: Graph):
    graph_copy = initGraphsForAuto(graph)
    res = count_isomorphisms_new([], [], graph, graph_copy)
    return res


# Sets of isomorphic graphs: Number of automorphisms:
# [0, 6]                     288
# [1, 5]                     576
# [1, 8, 9]

def testNewImpl(graphList: list[Graph], graph_index_mapping: list[int]):
    res = []
    visited = set()
    for graphId in graph_index_mapping:
        if graphId not in visited:
            group = [graph_index_mapping[graphId]]
            for otherId in graph_index_mapping:
               if graphId != otherId:
                   print(otherId)
                   print(f"compearing {graph_index_mapping[graphId]} to {graph_index_mapping[otherId]}res =")

                   isoREs = count_isomorphisms_new([], [], graphList[graphId], graphList[otherId])
                   # print(f"compearing {graph_index_mapping[graphId]} to {graph_index_mapping[otherId]}res = {isoREs}")
                   resBool = isoREs > 0
                   if resBool:
                       group.append(graph_index_mapping[otherId])  # true id of graph
                       visited.add(otherId)
            res.append(group)


def findIsoInGraphList(graphList: list[Graph], graph_index_mapping: list[int]):
    res = []
    visited = set()
    for i in range(len(graphList)):
        if i not in visited:
            group = [graph_index_mapping[i]]  # true id at posstion #[1, 8, 9][i]
            visited.add(i)
            for j in range(i + 1, len(graphList)):
                isoREs = count_isomorphisms_new([], [], graphList[i], graphList[j])
                print(f"compearing {graph_index_mapping[i]} to {graph_index_mapping[j]}res = {isoREs}" )
                resBool = isoREs > 0
                if resBool:
                    group.append(graph_index_mapping[j])  # true id of graph
                    visited.add(j)
            res.append(group)
    return res


# [0, 3] 3 [[0, 3], [1, 8, 9] ,[...]]
# [1, 8, 9] 3
# [2, 4, 7] 6
# [5, 6] 6
def solve_graph_iso_auto(graph_objects: dict, previous_partition: list[tuple]):
    possibleIsoGraphs = [elem[0] for elem in previous_partition]
    res = []
    for mapping_list in possibleIsoGraphs:
        objects_list = [graph_objects[index] for index in mapping_list]
        resList = findIsoInGraphList(objects_list, mapping_list)  # [1, 8, 9]
        res.append(resList)
    return res


def testAuto():
    listAuto = []

    # with open("Test/basicAut1.gr") as f:
    #     g = load_graph(f)
    #     listAuto.append(g)

    with open("Test/basicAut2.gr") as f:
        g = load_graph(f)
        listAuto.append(g)

    solve_graph_automorphisms(listAuto, True)


def autoPrint(ret, graph_dict: dict, mode):
    print(ret)
    for listG in ret:
        for gr in listG:
            if mode:
                res = useAuto(graph_dict[gr[0]])
            else:
                res = useIso(graph_dict[gr[0]])
            print(f"{gr} : {res} \n")


def solve_aut_iso_problem(file_path: str, showAuto):  # in need of path to file with a graph list!!!!
    graph_dict, first_refinement = group_graphs_by_iso(file_path)

    ret = solve_graph_iso_auto(graph_dict, first_refinement)
    if showAuto:
        print("Isomorph Graphs: Number of automorphisms:")
        autoPrint(ret, graph_dict, False)
    else:
        print("Isomorph Graphs:")
        for group in ret:
            print(group)


if __name__ == '__main__':
    # testAuto()
    solve_aut_iso_problem('G:\python\Projects\graph_project\BranchingTestGraphs\modulesD.grl', True)
    # solve_graph_isomorphisms("Test/BasicGI1.grl")
    # solve_graph_isomorphisms("Test/BasicGI2.grl")
    # solve_graph_isomorphisms("Test/BasicGI3.grl")
