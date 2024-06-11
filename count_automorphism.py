# from typing import List
#
# from basicpermutationgroup import Reduce, Orbit, FindNonTrivialOrbit, Stabilizer
# from colorref import colorRefine, init_labels_with_degree, computeGroupsOfVertexes
# from count_isomorphism import is_bijection, store_graph_snapshot, choose_color_class, assign_new_color, \
#     restore_graph_from_snapshot, is_unbalanced
# from graph import Edge
# from graph import Graph, Vertex
# from graph_io import write_dot, load_graph
# from permTest import computeOrder, check_composition
# from permv2 import permutation
#
#
# def naiveCheck(X_list, permToTest):  # true if it exist in X
#     for perm in X_list:
#         if perm == permToTest:
#             return True
#
#     return False
#
#
# #
# # def testMembershipOfPermutation(permToTest, X_list):
# #     if len(X_list) == 0:
# #         print(f"ADDING NEW PERM {permToTest}")
# #         X_list.append(permToTest)
# #         return
# #     # print(permToTest)
# #     if naiveCheck(X_list, permToTest):
# #         print(f"naiveCheck not adding {permToTest} to X_list {X_list}")
# #         return
# #
# #     nonTrivOrb = FindNonTrivialOrbit(X_list)
# #     orbitZero, transversalZero = Orbit(X_list, nonTrivOrb, True)
# #     stabilizer_subgroup = Stabilizer(X_list, nonTrivOrb)
# #
# #     if len(stabilizer_subgroup) == 0:
# #         X_list.append(permToTest)
# #         return
# #     funcCompos = stabilizer_subgroup[0] * permToTest
# #     print(funcCompos)
# #     print(f"stabilizer_subgroup {stabilizer_subgroup}")
# #     if checkComposition(funcCompos, transversalZero):
# #         X_list.append(permToTest)
# #         print(f"perm {permToTest} added to X_list {X_list}")
# #     else:
# #         print("Its not unique ")
#
#
# def compute_cycle(D_list, I_list):
#     res_cycle = []
#     if len(D_list) != len(I_list):
#         print("wrong")
#     for i in range(len(D_list)):
#         xId = D_list[i].id
#         yId = I_list[i].id
#
#         if xId != yId:
#             cycle = [xId, yId]
#             res_cycle.append(cycle)
#     print(res_cycle)
#     return res_cycle
#
#
# def compareToListX(cyclePerm):  # true if there is this cycle in X list
#     for perm in X_list:
#         if perm == cyclePerm:
#             return True
#     return False
#
#
# def memberShipCheckBijection(D_list, I_list):
#     cycle = compute_cycle(D_list, I_list)
#     cyclePerm = permutation(n=NumberOfVertices, cycles=cycle)
#     print(cyclePerm)
#     if not cyclePerm.istrivial():
#         if not compareToListX(cyclePerm):
#             stab = Stabilizer(X_list,0)
#             if len(stab) == 0:
#                 X_list.append(cyclePerm)
#                 return
#             print(f"Stabilizer {stab}")
#             if check_composition(cyclePerm, stab):
#                 print(f"Adding {cyclePerm} to X_list {X_list}")
#                 X_list.append(cyclePerm)
#
# #
# # def pruningBranchNew(D_list, I_list):
# #     if len(X_list) >= 1:
# #         cycle = computeCycle(D_list, I_list)
# #         permToTest = permutation(n=NumberOfVertices, cycles=cycle)
# #         nonTrivOrb = FindNonTrivialOrbit(X_list)
# #         orbitZero, transversalZero = Orbit(X_list, nonTrivOrb, True)
# #         stabilizer_subgroup = Stabilizer(X_list, nonTrivOrb)
# #         print(stabilizer_subgroup)
# #         if len(stabilizer_subgroup) == 0:
# #             return False
# #         if len(stabilizer_subgroup) >= 1:
# #             funcCompos = stabilizer_subgroup[0] * permToTest
# #             if checkComposition(funcCompos, transversalZero):
# #                 return False
# #         print("pruningBranchNew returnts true")
# #         return True
#
#
# def optimise_cycles(resCycle: list) -> list or None:
#     used_ids = set()
#     for cycle in resCycle:
#         for elem in cycle:
#             if len(cycle) != 0:
#                 if elem not in used_ids:
#                     used_ids.add(elem)
#                 else:
#                     return None
#
#     return resCycle
#
#
# def get_ids_from_vertices(vertices: list[Vertex]) -> list[int]:
#     res = []
#     for vertex in vertices:
#         res.append(vertex.id)
#     return res
#
#
# def simple_generating_set(D_list: List[Vertex], I_list: List[Vertex], g1: Graph, g2: Graph):
#     global NumberOfVertices  # TODO
#     global X_list
#
#     colorRefine(g1)
#     colorRefine(g2)
#
#     first_color_group_dict = store_graph_snapshot(g1)
#     second_color_group_dict = store_graph_snapshot(g2)
#
#     if is_unbalanced(first_color_group_dict, second_color_group_dict):
#         return 0
#     if is_bijection(g1, g2):
#         print("Bijection Hit ")
#         memberShipCheckBijection(D_list, I_list)
#         return 1
#
#     if len(D_list) >= len(g1.vertices):
#         return 0
#     color_key = choose_color_class(first_color_group_dict)
#     D_list, I_list = D_list[:], I_list[:]
#     color_group_g_one = first_color_group_dict[color_key]
#     color_group_g_two = second_color_group_dict[color_key]
#     sort_vertices_by_id(color_group_g_two)
#     vert_x = choose_lowest_by_id(color_group_g_one, D_list, I_list)
#
#     assign_new_color(vert_x, g1)
#     D_list.append(vert_x)
#
#     snap_shot_g1 = store_graph_snapshot(g1)  # TODO
#     snap_shot_g2 = store_graph_snapshot(g2)
#
#     print(get_ids_from_vertices(D_list))
#     for vertY in color_group_g_two:
#         if vertY in I_list[:-1] or vertY.id in get_ids_from_vertices(D_list[:-1]):
#             vertY = find_vertex_alternative(vertY,D_list[:-1],I_list[:-1])
#
#         if not vertY is None:
#             I_list.append(vertY)
#             vertY.label = vert_x.label
#             simple_generating_set(D_list, I_list, g1, g2)
#             restore_graph_from_snapshot(snap_shot_g1, snap_shot_g2)  # TODO
#             I_list.remove(vertY)
#
#
# def sort_vertices_by_id(vertex_list: List[Vertex]) -> List[Vertex]:
#     return sorted(vertex_list, key=lambda vertex: vertex.id)
#
#
# def choose_lowest_by_id(vertex_list: List[Vertex], D: list, I: list) -> Vertex:
#     # print("CHOOSING X")
#     # print(f"D {[vertex.id for vertex in D]}")
#     # print(f"I {[vertex.id for vertex in I]}")
#     vertex_list = sort_vertices_by_id(vertex_list)
#     # print(f"Choosing X among {vertex_list}")
#     for vert in vertex_list:
#         if find_vertex_alternative(vert, D, I) is not None:
#             print(I.__contains__(vert))
#             # print(vert.)
#             # print(I)
#             # print(vert.id)
#             return find_vertex_alternative(vert, D, I)
#
#
# def vertex_already_mapped(vertex: Vertex, D: list, I: list) -> bool:
#     for v in D:
#         if vertex.id == v.id:
#             return True
#     for v in I:
#         if vertex.id == v.id:
#             return True
#     return False
#
#
# def find_vertex_alternative(vertex: Vertex, d: list, i: list) -> Vertex or None:
#     if not vertex_already_mapped(vertex, d, i):
#         return vertex
#     orbit_of_x = Orbit(X_list, vertex.id)
#     if len(orbit_of_x) >= 2:
#         for v_id in orbit_of_x:
#             print(f"Comparing ids: {v_id} and {vertex.id}")
#             if v_id != vertex.id:
#                 return find_vertex_by_id(vertex.graph, v_id)
#                 # return vertex
#     return None
#
#
# class WrongGraphError(Exception):
#     def __init__(self, message="An empty graph is trying to be copied."):
#         self.message = message
#         super().__init__(self.message)
#
#
# def deep_copy_graph(color_map: dict) -> Graph:
#     if len(color_map) == 0:
#         raise WrongGraphError
#     highest_id = 0
#     vertex_neighbours_map = {}
#     is_simple = next(iter(color_map.values()))[0].graph.simple
#     is_directed = next(iter(color_map.values()))[0].graph.directed
#     graph_copy = Graph(n=0, simple=is_simple, directed=is_directed)
#     for key, vertices in color_map.items():
#         for vertex in vertices:
#             vertex.id = highest_id
#             vertex_copy = Vertex(graph_copy)
#             vertex_copy.id = highest_id
#             vertex_copy.label = key
#             vertex_neighbours_map[vertex_copy] = vertex.incidence
#             graph_copy.add_vertex(vertex_copy)
#             highest_id += 1
#     for vertex, edge_list in vertex_neighbours_map.items():
#         for edge in edge_list:
#             edge_tail_in_copy = find_vertex_by_id(graph_copy, edge.tail.id)
#             edge_head_in_copy = find_vertex_by_id(graph_copy, edge.head.id)
#             edge_to_add = Edge(edge_tail_in_copy, edge_head_in_copy)
#             if check_neighbours_for_copy(vertex, edge_to_add):
#                 graph_copy.add_edge(edge_to_add)
#     # Swap for example graph #TODO Remove swap REMOVE SWAP
#     #############################################################
#     # vert_3 = None
#     # vert_5 = None
#     # for vertex in graph_copy.vertices:
#     #     if vertex.id == 5:
#     #         vert_3 = vertex
#     #     if vertex.id == 3:
#     #         vert_5 = vertex
#     # vert_5.id = 5
#     # vert_3.id = 3
#     # for vertex in next(iter(color_map.values()))[0].graph.vertices:
#     #     if vertex.id == 5:
#     #         vert_3 = vertex
#     #     if vertex.id == 3:
#     #         vert_5 = vertex
#     # vert_5.id = 5
#     # vert_3.id = 3
#     # END OF THE SWAP ##################################################
#     return graph_copy
#
#
# def find_vertex_by_id(graph: Graph, vertex_id: int) -> Vertex or None:
#     for vertex in graph.vertices:
#         if vertex.id == vertex_id:
#             return vertex
#     return None
#
#
# def check_neighbours_for_copy(vertex: Vertex, edge: Edge) -> bool:
#     if edge.tail == vertex:
#         if edge.head.neighbours.__contains__(vertex):
#             return False
#     else:
#         if edge.tail.neighbours.__contains__(vertex):
#             return False
#     return True
#
#
# # def compute_order() -> int:
# #     list_of_perms = X_list
# #     for perm in list_of_perms:
# #         for el in perm:
# #             orbit_of_el = Orbit(X_list, el)
# #             if len(orbit_of_el) > 1:
# #                 orbit_trav = Orbit(X_list, el, returntransversal=True)
# #                 return len(orbit_trav[0]) * len(orbit_trav[1])
# #     return 1
# #     # what happens here !?
#
#
# def calculate_automorphisms(graph):
#     init_labels_with_degree(graph)
#     colorRefine(graph)
#     graphCopy = deep_copy_graph(
#         computeGroupsOfVertexes(graph))  # is copy before init_lables or not , depending on fast color reff
#     global X_list, NumberOfVertices
#     X_list = []
#     NumberOfVertices = len(graph.vertices)
#
#     simple_generating_set([], [], graph, graphCopy)
#     print("After simple_generating_set")
#     print(X_list)
#     reducedX = Reduce(X_list)
#     X_list = reducedX
#
#     defultPerm = permutation(NumberOfVertices,cycles=[[1,2]])
#     order = check_composition(defultPerm, reducedX)[1]
#     reducedX = Reduce(X_list)
#     X_list = reducedX
#     print(f"X list:  {X_list}")
#     return order
#
#
# def example_graph() -> Graph:
#     graph = Graph(False)
#     vert_list = []
#     for i in range(7):
#         vert = Vertex(graph, i)
#         vert_list.append(vert)
#         graph.add_vertex(vert)
#     zero_edges = []
#     for z in range(1, 7):
#         z_edge = Edge(vert_list[0], vert_list[z])
#         zero_edges.append(z_edge)
#         graph.add_edge(z_edge)
#
#     edge13 = Edge(vert_list[1], vert_list[3])
#     graph.add_edge(edge13)
#     edge32 = Edge(vert_list[3], vert_list[2])
#     graph.add_edge(edge32)
#     edge46 = Edge(vert_list[4], vert_list[6])
#     edge56 = Edge(vert_list[5], vert_list[6])
#     graph.add_edge(edge46)
#     graph.add_edge(edge56)
#
#     return graph
#
#
# def book_example():
#     test_graph = example_graph()
#     num_auto = calculate_automorphisms(test_graph)
#     print("RES")
#     print(X_list)
#     print(num_auto)
#
#
# def runFile():
#     with open('BranchingTestGraphs/cubes3.grl') as file:
#         graphInstanceList, options = load_graph(file, read_list=True)
#         g1 = graphInstanceList[1]
#         numAut = calculate_automorphisms(g1)
#         print(numAut)
#         # with open('BranchingTestGraphs.dot','w') as outfile:
#         #     write_dot(g1,outfile)
#
#
# def main():
#     book_example()
#
#     # runFile()
#
#
# def label_graph_with_ids(graph: Graph):
#     for vertex in graph.vertices:
#         vertex.label = vertex.id
#
#
# if __name__ == "__main__":
#     main()
