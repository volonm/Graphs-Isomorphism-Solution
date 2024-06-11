import time
from typing import List

from graph import Graph, Vertex
from graph_io import load_graph


# Demchuk Sviatoslav s2889811

def init_labels_with_degree(graph: Graph):
    for vert in graph.vertices:
        vert.label = vert.degree
    # updateColors(graph)


def highest_degree(graph: Graph):
    highest_vertex = -1
    for vert in graph.vertices:
        if vert.degree > highest_vertex:
            highest_vertex = vert.degree
    return highest_vertex


def updateColors(graph: Graph):
    for vert in graph.vertices:
        vert.colornum = int(vert.label)


def colorRefine(graph: Graph):
    highestVertexIndex = highest_degree(graph)
    changed = True
    iterationNumber = 0
    while changed:

        iterationNumber += 1
        vertexGroups = computeGroupsOfVertexes(graph)
        changed = False
        toChange = {}
        for key in sorted(vertexGroups.keys(), reverse=True):
            currentVertexGroup = vertexGroups[key]
            if len(currentVertexGroup) > 1:
                uniqueVertexGroups = {}
                for vert in currentVertexGroup:
                    neighbors = computeVertexNeighbors(vert)
                    neighbors.sort(reverse=True)
                    neighborsTuple = tuple(neighbors)
                    if neighborsTuple in uniqueVertexGroups:
                        uniqueVertexGroups[neighborsTuple].append(vert)
                    else:
                        uniqueVertexGroups[neighborsTuple] = [vert]
                if len(uniqueVertexGroups) > 1:
                    smallestKey = min(uniqueVertexGroups.keys())
                    for uniqueGroupKey in sorted(uniqueVertexGroups.keys()):
                        if uniqueGroupKey != smallestKey:
                            highestVertexIndex += 1
                            for v in uniqueVertexGroups[uniqueGroupKey]:
                                # v.label = highestVertexIndex
                                if highestVertexIndex not in toChange:
                                    toChange[highestVertexIndex] = [v]
                                else:
                                    toChange[highestVertexIndex].append(v)
                                changed = True
        for newVertexId in toChange:
            for vertToChange in toChange[newVertexId]:
                vertToChange.label = newVertexId

    updateColors(graph)
    return iterationNumber


def computeVertexNeighbors(vertex: Vertex):
    vertexNeighbors = vertex.neighbours
    neighborsList = []
    for vert in vertexNeighbors:
        neighborsList.append(vert.label)
    neighborsList.sort(reverse=True)
    return neighborsList


def computeGroupsOfVertexes(graph: Graph) -> dict:
    vertexGroups = {}
    for vertex in graph.vertices:
        if vertex.label in vertexGroups:
            vertexGroups[int(vertex.label)].append(vertex)
        else:
            vertexGroups[int(vertex.label)] = [vertex]
    return vertexGroups


def computeUniqueGraphIdentification(graph: Graph):
    vertexIdMap = {}
    knownLabels = set()
    labelCount = {}
    discrete = True
    for vert in graph.vertices:
        vertLabel = vert.label
        if vertLabel in knownLabels:
            discrete = False
            labelCount[vertLabel] += 1
        else:
            knownLabels.add(vertLabel)
            labelCount[vertLabel] = 1
        vertexIdMap[vertLabel] = computeVertexNeighbors(vert)
    return vertexIdMap, discrete, labelCount


def findPossibleIsomorphisms(graphList: List[Graph]):
    result = []
    tupleResult = []
    index = 0
    for graph in graphList:
        init_labels_with_degree(graph)
        iterNum = colorRefine(graph)
        # fast_colorref(graph)
        # iterNum = 0
        graphIdentification, discrete, labelCount = computeUniqueGraphIdentification(graph)
        if len(result) == 0:
            entryList = [[0], iterNum, discrete]
            entry = entryList
            result.append(entry)
        else:
            found = False
            for indexToCompare in range(index):
                existingGraphIdentification, existingDiscreteParam, existingLabelCount = (
                    computeUniqueGraphIdentification(graphList[indexToCompare]))
                sameVertexNumber = len(graphList[index].vertices) == len(graphList[indexToCompare].vertices)
                neighborsMapping = compareGraphIdentification(graphIdentification, existingGraphIdentification)
                vertexLabelCount = compareGrapLabelCount(labelCount, existingLabelCount)
                if neighborsMapping and vertexLabelCount and sameVertexNumber:
                    for resultEntry in result:
                        breakLoops = False
                        for graphIndex in resultEntry[0]:
                            if graphIndex == indexToCompare and discrete == existingDiscreteParam:
                                resultEntry[0].append(index)
                                if resultEntry[1] < iterNum:
                                    resultEntry[1] = iterNum
                                breakLoops = True
                                found = True
                                break
                        if breakLoops:
                            break
                if found:
                    break

            if not found:
                entryList = [[index], iterNum, discrete]
                entry = entryList
                result.append(entry)
        index += 1

    for res in result:
        tupleResult.append(tuple(res))
    return tupleResult


def compareGrapLabelCount(labelCount1, labelCount2):
    if len(labelCount1) != len(labelCount2):
        return False

    for key in labelCount1:
        if key not in labelCount2:
            return False

        if labelCount1[key] != labelCount2[key]:
            return False
    return True


def compareGraphIdentification(dict1, dict2):
    if len(dict1) != len(dict2):
        return False

    for key in dict1:
        if key not in dict2:
            return False
        if sorted(dict1[key]) != sorted(dict2[key]):
            return False

    return True


test_instances = ['colorref_largeexample_4_1026.grl',
                  'colorref_largeexample_6_960.grl',
                  'colorref_smallexample_2_49.grl',
                  'colorref_smallexample_4_16.grl',
                  'colorref_smallexample_4_7.grl',
                  'colorref_smallexample_6_15.grl',
                  'cref9vert3comp_10_27.grl',
                  'test_3reg.grl',
                  'test_cref9.grl',
                  'test_cycles.grl',
                  'test_empty.grl',
                  'test_iter.grl',

                  ]

# testPath = test_instance[4]

listFs = [1, 2, 3, 4, 5, 6]



def processGraphs(graphInstanceList, filename):
    print(f'Processing file: {filename}')
    print("Sets of possibly isomorphic graphs:")
    start_time = time.time()
    result = findPossibleIsomorphisms(graphInstanceList)
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    print(result)
    print("")
    print(f"Execution time: {execution_time:.5f} milliseconds")
    print("\n\n")


def main():
    runList = True
    if runList:  # 'SampleGraphsBasicColorRefinement/{path}'
        for path in test_instances:  # f'ddw/cref_signoff{path}_wk3.grl'
            with open(f'SampleGraphsBasicColorRefinement/{path}') as file:
                graphInstanceList, options = load_graph(file, read_list=True)
                processGraphs(graphInstanceList, path)


if __name__ == "__main__":
    main()


def basic_colorref(filePath):
    with open(filePath) as file:
        graphInstanceList, options = load_graph(file, read_list=True)
        res = findPossibleIsomorphisms(graphInstanceList)
        return res

# print(basic_colorref('SampleGraphsBasicColorRefinement/test_trees.grl'))
