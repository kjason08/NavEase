import numpy as np
import math
import json

#테스트 예제: 카이스트~신세계 백화점까지의 노드 데이터 -> closedList: [0, 2, 1, 3, 4, 5, 6, 7]
file_path = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/markers_SSG.json"
with open(file_path, 'r') as file:
    data_SSG = json.load(file)

#인접 여부 데이터
AMatrix_SSG = [[0,1,1,0,0,0,0,0,0,0,0,0],[1,0,0,1,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,1,0,0,0],
                  [0,1,1,0,1,0,0,0,0,0,0,0],[0,0,0,1,0,1,0,0,0,0,0,0],[0,0,0,0,1,0,1,0,0,0,0,1],
                  [0,0,0,0,0,1,0,1,0,0,0,1],[0,0,0,0,0,0,1,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,1,0,0],
                  [0,0,0,0,0,0,0,0,1,0,1,0],[0,0,0,0,0,0,0,0,0,1,0,1],[0,0,0,0,0,1,1,0,0,0,1,0]]

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

#Heuristic 값: 직선 거리에 대한 도보 속력
def getHeuristic(node, current, goal):
    currentNode = node[current]
    goalNode = node[goal]
    lat1 = currentNode['lat']
    lon1 = currentNode['lng']
    lat2 = goalNode['lat']
    lon2 = goalNode['lng']

    #직선 거리 계산
    h = getDistance(lat1, lon1, lat2, lon2)

    return h

#G 값: 노드 간 비용 (이동 불편도)
#변수 설명: 노드 구조 list, 인접 행렬, 부모 노드 인덱스, 인접 노드 인덱스, 모빌리티 인덱스 구분자 (1~10000)
def getDiscomfort(node, AMatrix, parent, adjacent, mobility_index_delimiter):
    #인접한 노드
    adjacentNode = node[adjacent]
    #현재 노드
    parentNode = node[parent]

    #인접 여부 확인
    adjacencyVector = AMatrix[parent]
    adjacency = adjacencyVector[adjacent]
    if adjacency == 0:
        return math.inf
    else:
        #노드 사이 거리 계산
        adjacentLocation = [adjacentNode['lat'], adjacentNode['lng']]
        parentLocation = [parentNode['lat'], parentNode['lng']]
        distance = getDistance(adjacentLocation[0], adjacentLocation[1], parentLocation[0], parentLocation[1])

        #이용 가능한 교통 자원
        adjacentM = adjacentNode['customValue']
        parentM = parentNode['customValue']
        #이동 소요 시간
        passingTime = math.inf
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
    lineData_str = str(R_bus)
    numberBusLine = len(lineData_str) - 2
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

#open list, closed list에 들어갈 노드 구조체 리스트 생성
def nodeStructure(node, AMatrix, goalIndex, adjacentIndex, parentIndex, parentStructure):
    structureList = []
    for i in delimiters:
        structure = dict()
        structure['G'] = getDiscomfort(node, AMatrix, parentIndex, adjacentIndex, i) + parentStructure['G']
        structure['H'] = getHeuristic(node, adjacentIndex, goalIndex)
        structure['F'] = structure['G'] + structure['H']
        structure['id'] = adjacentIndex
        if structure['F'] != math.inf:
            structure['ParentNode'] = parentIndex
            structureList.append(structure)

    return structureList

# A* 알고리즘
def aStar(node, AMatrix, start, end):
    #반복 횟수
    iter = 0

    #openList, closedList 초기화
    openList = []
    closedList = []
    openIndexList = []
    closedIndexList = []

    # closedList에 시작 노드 추가
    startStructure = {'G' : 0, 'H': 0, 'ParentNode' : 0, 'id' : start}
    closedList.append(startStructure)
    closedIndexList.append(start)

    # 현재 노드 초기화
    currentNode = node[start]
    currentIndex = start
    #현재 노드에서의 인접 벡터 초기화
    currentVector = AMatrix[currentIndex]
    #부모 노드 초기화
    parentStructure = startStructure

    # closedList에 end Node가 들어갈 때까지 실행
    while {'state' : 'finished'} not in closedList:
        #openList에 인접한 노드 추가: 인접해있으면서 closedList에 있지 않아야 한다
        for w in range(1,len(currentVector)):
            adjacentIndex = w - 1
            adjacency = currentVector[adjacentIndex]
            if adjacency != 0 and adjacentIndex not in closedIndexList:
                #인접한 노드에 대한 구조 리스트 생성
                newStructureList = nodeStructure(node, AMatrix, end, adjacentIndex, currentIndex, parentStructure)
                #newStructureList에서 가장 작은 F값을 갖는 구조체 찾기 
                fList = []
                for s in newStructureList:
                    fList.append(s['F'])
                minF = min(fList)
                minIndex = fList.index(minF)
                newStructure = newStructureList[minIndex]
                #인접한 노드가 openList의 기존에 있는 값보다 작은 F값을 가지는 경우 대체
                if adjacentIndex in openIndexList:
                    originalIndex = openIndexList.index(adjacentIndex)
                    originalNode = openList[originalIndex] 
                    if newStructure['F'] < originalNode['F']:
                        openList.remove(originalNode)
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
        #최소 F값을 가지는 노드 closedList에 추가
        for n in openList:
            if n['F'] == minFValue:
                closedList.append(n)
                #최소 F값을 가지는 노드의 id
                minimalIndex = n['id']
                closedIndexList.append(minimalIndex)
                #현재 노드 설정
                currentNode = node[minimalIndex]
                currentIndex = minimalIndex
                #현재 인접 벡터 설정
                currentVector = AMatrix[currentIndex]
                #부모 노드 설정
                parentStructure = n
                #openList에 있던 것 제거
                openIndexList.remove(currentIndex)
                openList.remove(n)
                #End Node가 추가되었을 때 closedList에 {'state' : 'finished'} 추가
                if currentIndex == end:
                    closedList.append({'state' : 'finished'})
                break
        iter += 1
        if iter > 10000:
            print("경로를 찾는 데 시간이 너무 많이 듭니다.")
            print(closedIndexList)
            print(closedList)
            break

    #closedList와 closedIndexList 반환
    return [closedList, closedIndexList]

#최단 경로를 표출
def describeShortestPath(node, AMatrix, start, end):
    closedListList = aStar(node, AMatrix, start, end)
    closedList = closedListList[0]
    closedList.remove({'state' : 'finished'})
    closedIndexList = closedListList[1]

    shortestPath = []
    shortestPathId = []
    #서로 다른 경로 세트를 담을 dictionary
    fSet = dict()
    i = 0
    parent = math.inf

    #Parent Node에 따라 경로 분류
    for n in closedList:
        if n['id'] == start:
            shortestPath.append(n)
            shortestPathId.append(start)
            parent = start
        else:
            if n['ParentNode'] == parent:
                shortestPath.append(n)
                shortestPathId.append(n['id'])
                fSet[str(i)] = n['F']
                fSet[str(i) + 'Path'] = shortestPath
                fSet[str(i) + 'Id'] = shortestPathId
                parent = n['id']
            else:
                i += 1
                shortestPath = []
                shortestPathId = []
                parent = n['ParentNode']
                parentNode = {'id' : parent}
                #이전 path를 역추적
                while parentNode['id'] != start:
                    for c in closedList:
                        if c['id'] == parent:
                            parentNode = c
                            shortestPath.append(parentNode)
                            shortestPathId.append(parent)
                            parent = parentNode['ParentNode']
                    shortestPath.append(parentNode)
                    shortestPathId.append(parent)
                shortestPath.append(closedList[0])
                shortestPathId.append(closedList[0]['id'])
                shortestPath.reverse()
                shortestPathId.reverse()
                shortestPath.append(n)
                shortestPathId.append(n['id'])
                fSet[str(i)] = n['F']
                fSet[str(i) + 'Path'] = shortestPath
                fSet[str(i) + 'Id'] = shortestPathId
                parent = n['id']
    #가장 작은 F값을 가지는 경로 호출
    minPathValue = math.inf
    for k in range(0, i + 1):
        keyI = str(k)
        if fSet[keyI] < minPathValue:
            minPathValue = fSet[keyI]
    for k in range(0, i + 1):
        if fSet[keyI] == minPathValue:
            return [fSet[keyI + 'Path'], fSet[keyI + 'Id']]

print(aStar(data_SSG, AMatrix_SSG, 0, 7)[0])
print(describeShortestPath(data_SSG, AMatrix_SSG, 0, 7)[1])