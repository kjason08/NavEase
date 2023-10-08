import numpy as np
import math
import json

#카이스트~신세계 백화점까지의 노드 데이터
#각 노드에 대한 위도, 경도 데이터를 markers.json 파일에서 가져오는 함수
def getLocation():
    #markers.json 파일 열기
    file_path = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/markers_SSG.json"
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
mobility_Index = [0,10001,0,10001,10001,10001,0,0,0,0,0,0]
delimiters = [10000, 1000, 100, 10, 1]

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

#위도, 경도 기반 거리 계산: 맨하튼 거리
def getManhattan(lat1, lon1, lat2, lon2):
    d1 = getDistance(lat1, lon1, lat2, lon1)
    d2 = getDistance(lat2, lon1, lat2, lon2)

    return d1 + d2

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
                if mobility_Index[indexI]//100 == 0:
                    takingTime = distance/v_walk
                elif mobility_Index[indexI]//100 == 3:
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

#Heuristic 값: 맨해튼 거리에 대한 도보 속력
def getHeuristic(node, current, goal):
    currentNode = node[current]
    goalNode = node[goal]
    lat1 = currentNode['lat']
    lon1 = currentNode['lng']
    lat2 = goalNode['lat']
    lon2 = goalNode['lng']

    #맨해튼 거리 계산
    h = getManhattan(lat1, lon1, lat2, lon2)

    return h

#G 값: 노드 간 비용 (이동 불편도)
#변수 설명: 노드 구조 list, 인접 행렬, 부모 노드 인덱스, 인접 노드 인덱스, 모빌리티 인덱스 구분자 (1~10000)
def getDiscomfort(node, AMatrix, parent, adjacent, mobility_index_delimiter):
    #인접한 노드
    adjacentNode = node[adjacent]
    #현재 노드
    parentNode = node[parent]

    #인접 여부 확인
    adjacencyVector = AMatrix[node.index(parentNode)]
    adjacency = adjacencyVector[node.index(adjacentNode)]
    if adjacency == math.inf:
        return math.inf
    else:
        #노드 사이 거리 계산
        adjacentLocation = [adjacentNode['lat'], adjacentNode['lng']]
        parentLocation = [parentNode['lat'], parentNode['lng']]
        distance = getManhattan(adjacentLocation[0], adjacentLocation[1], parentLocation[0], parentLocation[1])

        #이용 가능한 교통 자원
        adjacentM = adjacentNode['customValue']
        parentM = parentNode['customValue']
        if mobility_index_delimiter == 10000:
            Q_walk_parent = parentM//mobility_index_delimiter
            Q_walk_adjacent = adjacentM//mobility_index_delimiter
            if Q_walk_parent == 1:
                #인접 노드로 걸어서 이동할 수 있는지 확인
                if Q_walk_adjacent == 1:
                    passingTime = distance/v_walk
                else:
                    passingTime = math.inf
            else:
                passingTime = math.inf
        elif mobility_index_delimiter == 1000:
            Q_tashu = (parentM%10000)//mobility_index_delimiter
            if Q_tashu == 1:
                #인접 노드도 타슈(자전거)로 이용 가능한 지 확인
                if ((parentM%10000)%1000)//100 == 1 and ((adjacentM%10000)%1000)//100 == 1:
                    passingTime = distance/v_bike
                else:
                    passingTime = math.inf
            else:
                passingTime = math.inf
        elif mobility_index_delimiter == 100:
            Q_bicycle_parent = ((parentM%10000)%1000)//mobility_index_delimiter
            Q_bicycle_adjacent = ((adjacentM%10000)%1000)//mobility_index_delimiter
            if Q_bicycle_parent == 1:
                #인접 노드로 자전거를 타고 이동할 수 있는지 확인
                if Q_bicycle_adjacent == 1:
                    passingTime = distance/v_bike
                else:
                    passingTime = math.inf
            else:
                passingTime = math.inf
        elif mobility_index_delimiter == 10:
            Q_subway_parent = (((parentM%10000)%1000)%100)//mobility_index_delimiter
            Q_subway_adjacent = (((adjacentM%10000)%1000)%100)//mobility_index_delimiter
            if Q_subway_parent == 1:
                #인접 노드로 지하철을 타고 이동할 수 있는지 확인
                if Q_subway_adjacent == 1:
                    passingTime = distance/v_subway
                else:
                    passingTime = math.inf
            else:
                passingTime = math.inf
        elif mobility_index_delimiter == 1:
            R_bus_parent = (((parentM%10000)%1000)%100)%10
            R_bus_adjacent = (((adjacentM%10000)%1000)%100)%10
            if R_bus_parent > 0:
                #인접 노드로 버스를 타고 이동할 수 있는지 확인
                if R_bus_adjacent > 0:
                    #버스 노선이 일치하는지 확인
                    if len(getCommmonBusLine(R_bus_parent, R_bus_adjacent)) > 0:
                        #노선마다 대기 시간 비교 필요
                        passingTime = distance/v_bus
                    else:
                        passingTime = math.inf
                else:
                    passingTime = math.inf
        else:
            #잘못된 mobility_index_delimeter
            print("Wrong mobility index delimeter is put")
            passingTime = math.inf
    
    #혼잡도, 비용 등 적용 필요
    g = passingTime

    return g

#R_bus로부터 다니는 버스 노선 얻기
def getBusLine(R_bus):
    numberBusLine = len(R_bus) - 2
    lineData_str = str(R_bus)
    lineData = []
    for i in range(1, numberBusLine):
        if lineData_str[i + 1] == 1:
            lineData.append(i)
    return lineData

#두 노드를 지나는 버스 노선이 있는지 확인
def getCommmonBusLine(R_bus_1, R_bus_2):
    lineData_1 = getBusLine(R_bus_1)
    lineData_2 = getBusLine(R_bus_2)
    #교집합 확인
    intersection = set(lineData_1) & set(lineData_2)
    
    return list(intersection)

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

#print(aStar(data_SSG, isAdjacent_SSG, 0, 7)[1])




            