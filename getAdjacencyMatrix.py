import numpy as np
import math
import json

#카이스트~신세계 백화점까지의 노드 데이터
#각 노드에 대한 위도, 경도 데이터를 markers.json 파일에서 가져오는 함수
def getLocation():
    #markers.json 파일 열기
    file_path = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/markers.json"
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    #각 노드의 dictionary를 list로 변환
    location = []
    nodeLocation = []
    for i in data:
        nodeLocation = [i['lat'],i['lng']]
        location.insert(i['number']-1,nodeLocation)
        nodeLocation = []
    return location

data_SSG = getLocation()

arr_SSG = np.array(data_SSG)

#인접 여부 데이터
isAdjacent_SSG = [[0,1,1,0,0,0,0,0,0,0,0,0],[1,0,0,1,1,1,1,0,0,0,0,0],[1,0,0,0,0,0,0,0,1,0,0,0],
                  [0,1,0,0,1,0,0,0,0,0,0,0],[0,0,0,1,0,1,0,0,0,0,0,0],[0,0,0,0,1,0,1,0,0,0,0,0],
                  [0,0,0,0,0,1,0,1,0,0,0,1],[0,0,0,0,0,0,1,0,0,0,0,1],[0,0,1,0,0,0,0,0,0,1,0,0],
                  [0,0,0,0,0,0,0,0,1,0,1,0],[0,0,0,0,0,0,0,0,0,1,0,1],[0,0,0,0,0,0,1,0,0,0,1,0]]

#모빌리티 인덱스
mobilityIndex = [0,300,0,300,300,300,0,0,0,0,0,0]

#모빌리티 인덱스에 따른 속력
v_walk = 5
v_bike = 15
v_bus = 20
v_subway = 100

#위도, 경도 기반 거리 계산: 하버사인 공식
def getDistance(lat1, lon1, lat2, lon2):
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    havLat = math.pow(math.sin(dLat/2), 2)
    havLon = math.pow(math.sin(dLon/2), 2)
    #지구 반지름(km)
    R = 6371
    distance = 2 * R * math.asin(math.sqrt(havLat + math.cos(lat1) * math.cos(lat2) * havLon))
    return distance

#Weighted directed adjacency matrix 생성
def getWDAdjacency(location, isAdjacency):
    A = []
    indexI = 0
    for n in isAdjacency:
        indexJ = 0
        adjacencyRow = []
        for adjacency in n:
            if adjacency == 1:
                distance = getDistance(location[indexI][0], location[indexI][1], 
                                                location[indexJ][0], location[indexJ][1])
                # distance -> time
                if mobilityIndex[indexI]//100 == 0:
                    takingTime = distance/v_walk
                elif mobilityIndex[indexI]//100 == 3:
                    takingTime = distance/v_bus
                else:
                    takingTime = distance/v_bike
               #adjacencyRow.append(getDistance(location[indexI][0], location[indexI][1], 
                                                #location[indexJ][0], location[indexJ][1]))
                adjacencyRow.append(takingTime)
            else:
                adjacencyRow.append(math.inf)
            indexJ += 1
        A.append(adjacencyRow)
        indexI += 1
    return A

#Heuristic matrix 생성: 직선거리에 대한 도보 속력
def heuristic(node, goal):
    goalNode = node[goal]
    H = []
    for n in node:
        H.append(getDistance(n[0], n[1], goalNode[0], goalNode[1])/v_walk)
    return H

#open list, closed list에 들어갈 노드 구조체 생성
def nodeStructure(adMatrix, heuristic, currentIndex, parentIndex, parentStructure):
    structure = dict()
    structure['G'] = adMatrix[parentIndex][currentIndex] + parentStructure['G']
    structure['H'] = heuristic[currentIndex]
    structure['F'] = structure['G'] + structure['H']
    structure['ParentNode'] = parentIndex
    return structure

# A* 알고리즘
def aStar(node, isAdjacency, start, end):
    # Weighted directed adjacency matrix 생성
    graph = getWDAdjacency(node, isAdjacency)

    #openList, closedList 초기화
    openList = []
    closedList = []
    openIndexList = []
    closedIndexList = []

    #Heuristic matrix 생성
    H = heuristic(node, end)

    # closedList에 시작 노드 추가
    startStructure = {'G' : 0, 'H': 0, 'ParentNode' : 0}
    closedList.append(startStructure)
    closedIndexList.append(start)

    # 현재 노드 초기화
    currentNode = graph[start]
    currentIndex = start
    #부모 노드 초기화
    parentStructure = startStructure

    # closedList에 end Node가 들어갈 때까지 실행
    while {'state' : 'finished'} not in closedList:
        #openList에 인접한 노드 추가: 인접해있으면서 closedList에 있지 않아야 한다
        for w in currentNode:
            adjacentIndex = currentNode.index(w)
            if w != math.inf and adjacentIndex not in closedIndexList:
                newStructure = nodeStructure(graph, H, adjacentIndex, currentIndex, parentStructure)
                #기존에 있는 값보다 작은 F값을 가지는 경우 대체
                if adjacentIndex in openIndexList:
                    originalIndex = openIndexList.index(adjacentIndex)
                    if newStructure['F'] < openList[originalIndex]['F']:
                        openList.remove(openList[originalIndex])
                        openIndexList.remove(originalIndex)
                        openList.append(newStructure)
                        openIndexList.append(adjacentIndex)
                else:
                    openList.append(newStructure)
                    openIndexList.append(adjacentIndex)

        #openList에서 가장 작은 F값을 가지는 노드를 closedList에 추가
        #초기 값
        minFValue = math.inf
        #최소 F값 구하기
        for n in openList:
            if n['F'] < minFValue:
                minFValue = n['F']
        #최소 F값을 가지는 노드 추가
        for n in openList:
            if n['F'] == minFValue:
                closedList.append(n)
                closedIndexList.append(openIndexList[openList.index(n)])
                #현재 노드 설정
                currentNode = graph[openIndexList[openList.index(n)]]
                currentIndex = openIndexList[openList.index(n)]
                #부모 노드 설정
                parentStructure = n
                #openList에 있던 것 제거
                openIndexList.remove(openIndexList[openList.index(n)])
                openList.remove(n)
                #End Node가 추가되었을 때 closedList에 {'state' : 'finished'} 추가
                if n['H'] == 0:
                    closedList.append({'state' : 'finished'})
                break

    #closedList와 closedIndexList 반환
    return [closedList, closedIndexList]

print(aStar(data_SSG, isAdjacent_SSG, 0, 7)[1])




            