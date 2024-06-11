from typing import List

from basicpermutationgroup import Orbit, Reduce, Stabilizer, FindNonTrivialOrbit
from permv2 import permutation


def oldTEst():
    # Create permutations
    P = permutation(5, cycles=[["0", "2", "1", "4", "3"]])
    Q = permutation(5, cycles=[["1", "2"], ["3", "4"]])

    # Perform operations
    R = Q * P  # [1, 2], [3, 4][0, 2, 1, 4, 3]

    S = P ** 2
    T = -P

    orbit = Orbit([P, Q], 2, True)
    print(orbit)
    # Access elements
    image = P[2]

    reduce = Reduce([P, Q], 3)

    stabilizer = Stabilizer([P, Q], 0)
    print(stabilizer)
    # Check properties
    is_trivial = Q.istrivial()
    are_equal = P == Q

    # Print results
    print("P:", P)
    print("Q:", Q)
    print("R:", R)
    print("S:", S)
    print("T:", T)
    print("Image of 3 under Q:", image)
    print("Is Q trivial?", is_trivial)
    print("Are P and Q equal?", are_equal)


def newTest():
    # (3, 6)(1, 4)(2, 5)
    rightTR = [[4, 5]]
    leftTR = [[1, 2]]
    flip = [[3, 6], [1, 4], [2, 5]]

    rightTriangleROtation = permutation(7, rightTR)
    leftTriangleROtation = permutation(7, leftTR)
    flipGraph = permutation(7, cycles=flip)

    currentXlist = [rightTriangleROtation, leftTriangleROtation, flipGraph]
    stab = Stabilizer(currentXlist, 5)
    print(stab)

    orbit = Orbit(currentXlist, 1, True)
    print(orbit)

    reduce = Reduce(currentXlist, 3)
    print(reduce)
    # missing elements of graph from example
    print(rightTriangleROtation * flipGraph)

    print(leftTriangleROtation * flipGraph)

    # print(rightTriangleROtation * (-rightTriangleROtation))

    print(flipGraph * rightTriangleROtation * leftTriangleROtation)
    print("##########################")
    nonTrivalOrbit = FindNonTrivialOrbit(currentXlist)
    print(nonTrivalOrbit)
    nonTrivalOrbit = 2
    print("Orbit")
    orbitForNonTriv = Orbit(currentXlist, nonTrivalOrbit, True)
    print(orbitForNonTriv)
    HsubAlfa = orbitForNonTriv[1]
    print(HsubAlfa)

    H_alpha_generators = Stabilizer(currentXlist, 0)
    H_alpha_size = len(H_alpha_generators)
    orbitSize = len(HsubAlfa)
    print(H_alpha_generators)
    print(H_alpha_size)
    print(H_alpha_size * orbitSize)


def test_2():
    # (3, 6)(1, 4)(2, 5)
    # rightTR = [[4, 5]]
    # leftTR = [[1, 2]]
    # flip = [[3, 6], [1, 4], [2, 5]]
    #
    # rightTriangleROtation = permutation(7, rightTR)
    # leftTriangleROtation = permutation(7, leftTR)
    # flipGraph = permutation(7, cycles=flip)

    x_list = []  # []

    # x1 = 3  y1 -> 3
    # x2 = 1  y2 -> 1
    # x3 = 4  y3 -> 4
    # is bijection entered!
    # membership testing, the bijection is [] so D I
    # Iterate through D , I to get the mapping.
    # If every vertex is mapped to itself, then it is a trivial mapping --> Ignore

    # return to the last visited trivial ancestor node

    #
    # UP in TREE
    # TEST x3 = 4
    firstOrbit = Orbit(x_list, 4, True)
    print(firstOrbit)
    # test orbit  orbit will be
    print("go to x3 = 4 y3 ->5")
    #
    # x3 = 4 y3 ->5
    # Test whether the bijection is unique depending on X [[4]x3 in D ,[5]y3 in I ] [4,5]
    # X becomes [[4,5]]
    last_chosen_x = 4
    firstPerm = permutation(n=7, cycles=[[4, 5]])
    x_list.append(firstPerm)
    print(firstPerm)
    # broadly

    # up in tree
    # if  x3 ,y3 = 6 in H_alfa -> if not go in recurcive

    print("go to (tree lvl - 1) level ")
    print(Orbit(x_list, last_chosen_x, True))
    # if there is None or empty list continue searching for this x
    # In our case there is an

    # UP in TREE1
    print("go to x2 = 1 y2 ->1")
    last_chosen_x = 1
    print(Orbit(x_list, last_chosen_x, True))
    # if there is None or empty list continue searching for this x

    print("go to x2 = 1 y2 ->2")
    print(Orbit(x_list, last_chosen_x, True))
    # print(Reduce(x_list,3))
    # REDUCE
    # Down in tree
    # keep Y2 = 2 not 1
    print("go to x3 = 4 y3 -> 4")
    # [1,2] x2 = 1 y2 = 2
    second_perm = permutation(n=7, cycles=[[1, 2]])
    x_list.append(second_perm)
    # print(x_list)
    # print(Reduce(x_list, 3))

    # UP in TREE
    print("go to x3 = 4 y3 -> 5")
    last_chosen_x = 4
    print(Orbit(x_list, last_chosen_x, True))
    # SO WE DONT GO IN the mapping x3 = 4 y3 -> 5

    # tree up x2 = 1
    print("go back to x2 = 1 y2 -> 2")
    last_chosen_x = 1
    print(Orbit(x_list, last_chosen_x, True))

    # tree up x1 = 3
    last_chosen_x = 3
    print(Orbit(x_list, last_chosen_x, True))

    # down tree x1 = 3 y1 = 6
    # down tree x2  =1 , y2 -> 4
    last_chosen_x = 1
    print(Orbit(x_list, last_chosen_x, True))

    # down tree x3 = 4 , y3 ->1
    # last bijection
    last_perm = permutation(n=7, cycles=[[3, 6], [1, 4], [2, 5]])
    x_list.append(last_perm)

    # go back to x3=4 and check y3=2
    last_chosen_x = 4
    print(Orbit(x_list, last_chosen_x, True))

    # go up in tree x2 = 1  y2 -> 5
    last_chosen_x = 1
    print(Orbit(x_list, last_chosen_x, True))


def small_perm_test():
    x_list = []

    first_perm = permutation(n=7, cycles=[[4, 6]])
    second_perm = permutation(n=7, cycles=[[1, 2]])
    third_perm = permutation(n=7, cycles=[[1, 2], [4, 5]])
    x_list.append(first_perm)
    x_list.append(second_perm)
    x_list.append(third_perm)

    print(x_list)
    fourth_perm = permutation(n=7, cycles=[[1, 2], [4, 6]])
    x_list.append(fourth_perm)
    print(x_list)
    print(Reduce(x_list))

    x_list.clear()
    first_perm = permutation(n=8, cycles=[[4, 5, 6, 7]])
    second_perm = permutation(n=8, cycles=[[5, 6, 7]])
    third_perm = permutation(n=8, cycles=[[6, 7]])
    x_list.append(first_perm)
    x_list.append(second_perm)
    x_list.append(third_perm)
    print("Second test")
    print(x_list)
    print(Reduce(x_list, wordy=3))


def testRed():
    first_perm = permutation(n=6, cycles=[[0, 1, 2], [4, 5]])
    second_perm = permutation(n=6, cycles=[[2, 3]])

    hRes = 0
    xList = [first_perm, second_perm]
    OrbitOfZero = Orbit(xList, 0, True)
    stab = Stabilizer(xList, 0)

    perm3 = permutation(n=6, cycles=[[2, 3]])
    perm4 = permutation(n=6, cycles=[[4, 5]])
    perm5 = permutation(n=6, cycles=[[1, 3]])
    print(OrbitOfZero)

    print(stab)

    redList = [perm3, perm4, perm5]
    orbit3 = Orbit(redList, 3, True)
    stan3 = Stabilizer(redList, 3)
    print(orbit3)
    print(stan3)

    perm6 = permutation(n=6, cycles=[[4, 5]])
    perm7 = permutation(n=6, cycles=[[1, 2]])

    genSet = [perm6, perm7]
    orbit4 = Orbit(genSet, 1)
    print(orbit4)
    stab5 = Stabilizer(genSet, 1)
    print(stab5)  # +2 Base case  return to redList # do we go one more step in recurssion
    print("WEQQ")
    # perm6 = permutation(n=6,cycles = [[]])
    print(FindNonTrivialOrbit([perm6]))
    print(perm6.istrivial())  # is one
    orbitOf4 = Orbit([perm6], 4, True)
    stabOf4 = Stabilizer([perm6], 4)
    print(orbitOf4)
    print(stabOf4)

    print("another branch ")
    redList = [perm3, perm4, perm5]
    orbit3 = Orbit(redList, 1, True)
    stan3 = Stabilizer(redList, 1)
    print(orbit3)
    print(stan3)  # +2 +2  6 for Halfa 0


def quikTest():
    orbitId = FindNonTrivialOrbit([])
    print(orbitId)


def computeOrder(permList):
    if len(permList) == 0:
        # print(f"Return one perm list empty {permList}\n\n ")
        return 1
    if len(permList) == 1:
        if permList[0].istrivial():
            return 1
    orderNum = 0
    orbitId = FindNonTrivialOrbit(permList)
    orbit = Orbit(permList, orbitId)

    for satellite in orbit:
        stabilizer = Stabilizer(permList, satellite)
        # print(f"For loop for orbit {orbit} current satellite {satellite}")
        # print(
        #     f"Current satellite {satellite} for orbit id  {orbitId} \n Stabilizer {stabilizer} \n, permList is {permList}\n")
        orderNum += computeOrder(stabilizer)
        # print(f"Current order {orderNum} for satellite {satellite}")

    return orderNum


def testOrder():
    # Test book 1
    prem1 = permutation(n=7, cycles=[[4, 5]])
    prem2 = permutation(n=7, cycles=[[1, 2]])
    prem3 = permutation(n=7, cycles=[[3, 6], [1, 4], [2, 5]])
    permList = [prem1, prem2, prem3]
    # Test book 2
    # prem1 = permutation(n=7, cycles=[[0,1, 2],[4,5]])
    # prem2 = permutation(n=7, cycles=[[2, 3]])
    # permList = [prem1, prem2]
    # Test book 3
    # prem1 = permutation(n=7, cycles=[[0, 1, 2,3,4,5]])
    # prem2 = permutation(n=7, cycles=[[1,5],[2,4]])
    # permList = [prem1, prem2]
    res = computeOrder(permList)
    print("computeOrder res")
    print(res)


def memberShip(perm: permutation, X_list: List[permutation]):
    if len(X_list) == 0:
        print(f"is added  {perm}")
        X_list.append(perm)
        return

    # if X_list.__contains__(perm):
    #     return
    orbitId = FindNonTrivialOrbit(X_list)
    orbit, transversal = Orbit(X_list, orbitId, returntransversal=True)
    stabilizer_subgroup = Stabilizer(X_list, orbitId)
    print(f' orbitId {orbitId} orbit {orbit} to transversal {transversal} , stabilizer subgroup {stabilizer_subgroup}')
    transversal_element = transversal[1]
    inverse_transversal = -transversal_element

    cycleComposition = inverse_transversal * perm
    print(f'cycleComposition is {cycleComposition} stabilizer_subgroup is {stabilizer_subgroup}')

    return False


# def check_composition(funcCompos, stabilizer_subgroup):
#     n = len(stabilizer_subgroup)
#     if n == 1:
#         return not funcCompos == stabilizer_subgroup[0]
#     matrix = [[[] for _ in range(n)] for _ in range(n)]
#     matrix[0][0] = [stabilizer_subgroup[0] * stabilizer_subgroup[0]]
#     # matrix[0][1] = stabilizer_subgroup[0] * stabilizer_subgroup[1]
#     for i in range(1, n):
#         temp_res_1 = []
#         temp_res_2 = []
#         for p in matrix[i - 1][0]:
#             temp_res_1.append(p * stabilizer_subgroup[i])
#             temp_res_1.append(stabilizer_subgroup[i])
#         for p in matrix[0][i - 1]:
#             temp_res_2.append(p * stabilizer_subgroup[i])
#             temp_res_2.append(stabilizer_subgroup[i])
#         # temp_res_1 = Reduce(temp_res_1)
#         # temp_res_2 = Reduce(temp_res_2)
#         matrix[i][0] = temp_res_1
#         matrix[0][i] = temp_res_2
#     for i in range(1, n):
#         for j in range(1, n):
#             temp_res = [stabilizer_subgroup[j]]
#             for perm in matrix[i - 1][j]:
#                 temp_res.append(perm * stabilizer_subgroup[j])
#             for perm in matrix[i][j - 1]:
#                 temp_res.append(stabilizer_subgroup[j] * perm)
#
#             # temp_res = Reduce(temp_res)
#             matrix[i][j] = temp_res
#             # matrix[i][j] = matrix[i - 1][j] * stabilizer_subgroup[j]
#             # matrix[i][j] = matrix[i][j - 1] * stabilizer_subgroup[j]
#     res = []
#     for i in range(n):
#         for j in range(n):
#             for perm in matrix[i][j]:
#                 if perm not in res:
#                     res.append(perm)
#     #
#
#     print_matrix(matrix)
#     print(f"HEY {matrix[n - 1][n - 1]}")
#     print(f"HEY Res {res}")
#     print(f"HEY Res len {len(res)}")
#     print(f"HEY {funcCompos}")
#     for perm in res:
#         if funcCompos == perm:
#             return False, len(res)
#     return True, len(res)


def print_matrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])

#
# def testMember():
#     prem1 = permutation(n=7, cycles=[[4, 5]])
#     prem2 = permutation(n=7, cycles=[[1, 2]])
#     prem3 = permutation(n=7, cycles=[[3, 6], [1, 4], [2, 5]])
#     X_list = [prem1, prem2, prem3]
#     testPerm = permutation(n=7, cycles=[[3, 6], [1, 4, 2, 5]])
#     nonTrivOrb = FindNonTrivialOrbit(X_list)
#     orbitZero, transversalZero = Orbit(X_list, nonTrivOrb, True)
#     stabilizer_subgroup = Stabilizer(X_list, nonTrivOrb)
#     # print(
#     #     f'{nonTrivOrb} - orbit {orbitZero} to transversal {transversalZero} , stabilizer subgroup {stabilizer_subgroup}')
#
#     funcCompos = stabilizer_subgroup[0] * testPerm
#     print(funcCompos)
#     print(f"stabilizer_subgroup {stabilizer_subgroup}")
#     if check_composition(funcCompos, transversalZero):
#         print("Element is unique and has to be added!!!!")
#     else:
#         print("Element is NOT unique")
#     # for orb in orbitZero:
#     # #     if orb != 0:
#     # nextOrbit, nextTransversal = Orbit(X_list, 4, True)  # for 3 (0,3,2)
#     # if len(nextOrbit) >= 2:
#     #     # print(nextOrbit)
#     #     newFuncCopos = nextTransversal[1] * testPerm
#     #     # print(newFuncCopos)
#     #     return


def naiveCheck(X_list, permToTest):  # true if it exist in X
    for perm in X_list:
        if perm == permToTest:
            return True

    return False

#
# def testMembershipOfPermutation(X_list, permToTest):
#     # print(permToTest)
#     if naiveCheck(X_list, permToTest):
#         print(f"naiveCheck not adding {permToTest} to X_list {X_list}")
#         return
#
#     nonTrivOrb = FindNonTrivialOrbit(X_list)
#     orbitZero, transversalZero = Orbit(X_list, nonTrivOrb, True)
#     stabilizer_subgroup = Stabilizer(X_list, nonTrivOrb)
#     funcCompos = stabilizer_subgroup[0] * permToTest
#     print(funcCompos)
#     print(f"stabilizer_subgroup {stabilizer_subgroup}")
#     if check_composition(funcCompos, transversalZero):
#         X_list.append(permToTest)
#         print(f"perm {permToTest} added to X_list {X_list}")
#     else:
#         print("Its not unique ")

import cProfile

# def memberShitCheck(X_list, permToTest):
#     if naiveCheck(X_list, permToTest):
#         return
#
#     if len(visitedOrbits) == 0:
#         nonTrivOrbitId = FindNonTrivialOrbit(X_list)
#         visitedOrbits.append(nonTrivOrbitId)
#         orbit, transversal = Orbit(X_list, nonTrivOrbitId, True)
#     else:
#         print(visitedOrbits)
#         newOrbitFound = False
#         i = 0
#         while not newOrbitFound:
#             try:
#                 nonTrivOrbitId = FindNonTrivialOrbit(X_list) + i
#                 i += 1
#                 orbit, transversal = Orbit(X_list, nonTrivOrbitId, True)
#             except IndexError:
#                 return
#             if nonTrivOrbitId not in visitedOrbits:
#
#                 if len(orbit) >= 2:
#                     newOrbitFound = True
#                     print("New orbit found:")
#                     visitedOrbits.append(nonTrivOrbitId)
#
#     stabilizer = Stabilizer(X_list, nonTrivOrbitId)
#     funcCompo = stabilizer[0] * permToTest
#     print(check_composition(funcCompo, ))
#     print(stabilizer)
#     print(funcCompo)
#     if check_composition(funcCompo, stabilizer):  # H_0 check
#         X_list.append(permToTest)
#         return
#     for sat in orbit:  # for all betta
#         if sat != nonTrivOrbitId:  # except of alfa
#             satOrbit, satTransversal = Orbit(X_list, sat, True)
#             # l = checkComposition(funcCompo, stabilizer)
#             print(l[0])
#             satStab = Stabilizer(X_list, sat)
#             # if len(satStab) == 0:
#             #     X_list.append(satOrbit)
#             #     return
#             satFuncComp = satStab[0] * permToTest
#             if check_composition(satFuncComp, satStab):
#                 X_list.append(permToTest)
#                 return
#
#     print(f" orbit {nonTrivOrbitId} transversal: {satTransversal}")
#     memberShitCheck(transversal, permToTest)


def testShit():
    prem1 = permutation(n=7, cycles=[[4, 5]])
    prem2 = permutation(n=7, cycles=[[1, 2]])
    # prem3 = permutation(n=7, cycles=[[3, 6], [1, 4], [2, 5]])
    X_list = [prem1, prem2]

    testPerm = permutation(n=7, cycles=[[1, 2], [4, 5]])
    global visitedOrbits
    visitedOrbits = []
    # memberShitCheck(X_list, testPerm)
    print(X_list)


# memberShip(prem1, X_list)
# print(X_list)

#
# nonTrivOrbit = FindNonTrivialOrbit(permList)
# print(nonTrivOrbit)
#
# orbitZero, transversalZero = Orbit(permList, 0, True)
# print(orbitZero)
# print(transversalZero)
# permToCheck = permutation(n=7, cycles=[[0, 2]])
# inversU2 = transversalZero[1]  # its class perm
# print(inversU2)
# compositionInversAndpermToChek = inversU2 * permToCheck
# print(type(compositionInversAndpermToChek))
# print(compositionInversAndpermToChek)


if __name__ == "__main__":
    # newTest()
    # oldTEst()
    # test_2()
    # small_perm_test()
    # testRed()

    # testOrder()
    # quikTest()
    # testMember()
    # testMember()
    # testMember()
    testShit()
