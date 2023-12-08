import math
import json
import sys, os
from getWaitingTime import WaitingTime
from Adjacency_Matrix import Adjacency
#Prediction 폴더 불러오기
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("Prediction/Occupancy"))))
from Prediction import Occupancy

WT = WaitingTime()
Adj = Adjacency()
OC = Occupancy.Occupancy()

#테스트 예제: 카이스트~신세계 백화점까지의 노드 데이터 -> closedList: [0, 1, 3, 4, 5, 6, 7]
file_path_SSG = "Astar/markers_SSG.json"
with open(file_path_SSG, 'r') as file:
    data_SSG = json.load(file)

#마커 데이터
file_path = "Markers/markers.json"
with open(file_path, 'r') as file:
    data = json.load(file)

#버스 노선
#bus_line_array = ["1", "3", "5", "11", "48", "101", "102", "104", "105", "106", "107", "108", "113", "114", "115", "116", "117", 
#"119", "121", "300", "312", "340", "342", "604", "655", "704", "705", "706", "911", "912", "1002", "1*",]
bus_line_array = ["5", "104", "105", "121", "911"]

#인접해있는 노드의 인덱스 정보만을 가지고 인접 행렬 생성
def getAdjacencyMatrix(adjacency_numbers):
    length = len(adjacency_numbers)
    adjacency_matrix = []
    for i in range(0, length):
        Ad = adjacency_numbers[i]
        A = []
        for j in range(0, length):
            if j in Ad:
                A.append(1)
            else:
                A.append(0)
        adjacency_matrix.append(A)
    return adjacency_matrix

#인접 여부 데이터
AMatrix_num = [[1,2,18],[0],[0,3,14],[2],[3],[4,6],[5,17,7],[6,7,8],[7,9],[8,10],[9,17],[10,17],[11],[12,14],[2,13,15],
               [14,16],[15,17],[11,6,10,16],[0,19],[13,18,14]]
AMatrix_SSG = Adj.getAdjacencyMatrix(AMatrix_num)
AMatrix = Adj.getAdjacencyMatrix(Adj.getIntergrated())

#모빌리티 인덱스
mobility_Index = [0, 10001, 0, 10001, 10001, 10001, 0, 0, 0, 0 ,0, 0]
delimiters = [10000, 1000, 100, 10, 1]

#사용자의 교통 선호도와 이용 가능한 교통 자원
global user_preference, mobility_availability
user_preference = 1
mobility_availability = delimiters
user1 = sys.argv[4]
user2 = sys.argv[5]
user3 = int(user1)
user4 = int(user2)
user5 = user4/10
user6 = user3+user5
user_preference = user6
mobility_availability = delimiters
list1 = sys.argv[3].split(',')

#교통 선호도 설정 함수
def setPreference(value):
    global user_preference
    if value < 1 or value > 2:
        user_preference = 1
    else:
        user_preference = value

#이용 가능한 교통 자원 설정: 이용하지 못하는 교통 자원의 인덱스 리스트로 입력
def setAvailability(list):
    global mobility_availability
    for i in list:
        if i in mobility_availability:
            mobility_availability.remove(i)
    return mobility_availability

mobility_availability = setAvailability(list1)

#모빌리티 인덱스에 따른 속력
v_walk = 5
v_bike = 15
v_bus = 20
v_subway = 100
v_Set = [v_walk, v_bike, v_bike, v_bus, v_subway]

#버스 대기가 필요한지에 대한 여부
global shouldWait
shouldWait = True

#현재 타고있는 버스와 다음에 탈 버스
global currentBusLine
currentBusLine = ""

#이용하고 있는 교통수단이 무엇인지 확인: 0 도보, 1 타슈, 2 자전거, 3 지하철, 4 버스
global mobility_type, line_type
mobility_type = []
line_type = []

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

#Mobility index로부터 이용 가능한 교통 자원 파악
def mToAvailability(mobilityIndex):
    result = []
    for i in range(0,5):
        result.append(mobilityIndex)
    result[0] = result[0]//10000
    result[1] = (result[1]%10000)//1000
    result[2] = ((result[2]%10000)%1000)//100
    result[3] = (((result[3]%10000)%1000)%100)//10
    result[4] = (((result[4]%10000)%1000)%100)%10

    return result

#Heuristic 값: 현재 위치에서 목적지까지의 직선 거리
def getHeuristic(node, current, goal):
    currentNode = node[current]
    goalNode = node[goal]
    lat1 = currentNode['lat']
    lon1 = currentNode['lng']
    lat2 = goalNode['lat']
    lon2 = goalNode['lng']

    #직선 거리 계산
    distance = getDistance(lat1, lon1, lat2, lon2)

    return distance

#이동 자원에 대한 가중치가 적용된 heuristic
def heuristicToTime(node, current, goal, mobility_index_delimiter):
    h = getHeuristic(node, current, goal)
    if mobility_index_delimiter == 10000:
        h = h/v_walk
    elif mobility_index_delimiter == 1000:
        h = h/v_bike
    elif mobility_index_delimiter == 100:
        h = h/v_bike
    elif mobility_index_delimiter == 10:
        h = h/v_subway
    elif mobility_index_delimiter == 1:
        h = h/v_bus
    else:
        h = math.inf
    
    return h

#waiting_line과 waiting_time, bus_stop_list를 채우는 함수
def checkBusStop(node, parent):
    #대기 시간 불러오기
    parentNode = node[parent]
    waiting_line = []
    waiting_time = []
    bus_stop = parentNode['stopValue']
    if bus_stop == "0":
        return [[], [], []]
    else:
        busLineList = WT.getLineList(bus_stop)
        busTimeList = WT.getMinDict(bus_stop)
        for i in busLineList:
            if i in bus_line_array:
                waiting_line.append(i)
                index = busLineList.index(i)
                waiting_time.append(busTimeList[index])

        return [waiting_line, waiting_time, bus_stop] 
                                               

#G 값: 노드 간 비용 (이동 시간)
#변수 설명: 노드 구조 list, 인접 행렬, 부모 노드 인덱스, 인접 노드 인덱스, 모빌리티 인덱스 구분자 (1~10000)
def getCost(node, AMatrix, parent, adjacent, mobility_index_delimiter):
    global currentBusLine
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
        #String
        adjacentM = adjacentNode['customValue']
        parentM = parentNode['customValue']
        #Int
        adjacentM_list = adjacentM.split('.')
        parentM_list = parentM.split('.')
        #소수점 앞 mobility index: 이용 가능한 교통 자원이 무엇인지 파악할 때 이용
        adjacentM = int(adjacentM_list[0])
        parentM = int(parentM_list[0])
        #소수점 뒤 mobility index: 이용 가능한 버스 노선이 무엇인지 파악할 때 이용
        R_bus_adjacent_str = adjacentM_list[1]
        R_bus_parent_str =parentM_list[1]

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
                    if len(getCommmonBusLine(R_bus_parent_str, R_bus_adjacent_str)) > 0:
                        passingTime = distance/v_bus
                    else:
                        passingTime = math.inf
                else:
                    passingTime = math.inf
        else:
            #잘못된 mobility_index_delimeter
            print("Wrong mobility index delimeter is put")
            passingTime = math.inf
    
    g = passingTime

    return g

#R_bus_str으로부터 다니는 버스 노선 얻기
def getBusLine(R_bus):
    numberBusLine = len(R_bus)
    lineData = []
    for i in range(0, numberBusLine):
        if R_bus[i] == "1":
            specific_line = bus_line_array[i]
            lineData.append(specific_line)
    return lineData

#두 노드를 지나는 버스 노선이 있는지 확인
def getCommmonBusLine(R_bus_1, R_bus_2):
    lineData_1 = getBusLine(R_bus_1)
    lineData_2 = getBusLine(R_bus_2)
    #교집합 확인
    intersection = set(lineData_1) & set(lineData_2)
    
    return list(intersection)

#이동 불편도 고려 X
#preference: 이동 양상에 대한 사용자 선호도
def getDiscomfort(node, AMatrix, parent, adjacent, mobility_index_delimiter, bus_stop, bus_line):
    global user_preference
    return getCost(node, AMatrix, parent, adjacent, mobility_index_delimiter)

#open list, closed list에 들어갈 노드 구조체 리스트 생성
#id: 노드 인덱스
#ParentNode: 전에 있었던 노드
#type: 이용하는 교통 자원
#G: 이동 비용
#H: 휴리스틱
#F: G + H
#line: 이용하는 버스 노선
#interval: 이 노드로 이동하는 스텝에서 소모되는 시간
def nodeStructure(node, AMatrix, goalIndex, adjacentIndex, parentIndex, parentStructure):
    global shouldWait, user_preference, mobility_availability
    structureList = []
    #사용자 이용 가능한 교통 자원 리스트 체크

    #대기 정보
    waiting_info_list = checkBusStop(node, parentIndex)
    waiting_line = waiting_info_list[0]
    waiting_time = waiting_info_list[1]
    bus_stop = waiting_info_list[2]
    for i in delimiters:
        structure = dict()
        structure['id'] = adjacentIndex
        structure['ParentNode'] = parentIndex
        structure['type'] = i
        #버스 노선 추가하기
        if i == 1:
            #가용한 노선마다 노드 구조 생성
            for l in waiting_line:
                #대기가 필요한 경우
                if shouldWait == True:
                    lIndex = waiting_line.index(l)
                    structure['G'] = getDiscomfort(node, AMatrix, parentIndex, adjacentIndex, i, bus_stop, l)
                    + parentStructure['G'] + waiting_time[lIndex] / 60
                    structure['interval'] = getCost(node, AMatrix, parentIndex, adjacentIndex, i) + waiting_time[lIndex] / 60
                    structure['line'] = l
                    shouldWait = False
                elif l != parentStructure['line']:
                    #버스를 갈아타는 경우
                    lIndex = waiting_line.index(l)
                    structure['G'] = getDiscomfort(node, AMatrix, parentIndex, adjacentIndex, i, bus_stop, l) 
                    + parentStructure['G'] + waiting_time[lIndex] / 60
                    structure['interval'] = getCost(node, AMatrix, parentIndex, adjacentIndex, i) + waiting_time[lIndex] / 60
                    structure['line'] = l
                else:
                    structure['G'] = getDiscomfort(node, AMatrix, parentIndex, adjacentIndex, i, bus_stop, l)
                    + parentStructure['G']
                    structure['interval'] = getCost(node, AMatrix, parentIndex, adjacentIndex, i)
                    structure['line'] = l
                if structure['G'] == math.inf:
                    structure['H'] = math.inf
                else:
                    structure['H'] = heuristicToTime(node, adjacentIndex, goalIndex, i)
                structure['F'] = structure['G'] + structure['H']
                structureList.append(structure)
        else:
            structure['G'] = getDiscomfort(node, AMatrix, parentIndex, adjacentIndex, i, bus_stop, "") + parentStructure['G']
            structure['interval'] = getDiscomfort(node, AMatrix, parentIndex, adjacentIndex, i, bus_stop, "")
            structure['line'] = ''
            if structure['G'] == math.inf:
                structure['H'] = math.inf
            else:
                structure['H'] = heuristicToTime(node, adjacentIndex, goalIndex, i)
            structure['F'] = structure['G'] + structure['H']
            structureList.append(structure)

    return structureList

# A* 알고리즘
def aStar(node, AMatrix, start, end):
    global shouldWait, mobility_type, line_type
    #반복 횟수
    iter = 0

    #openList, closedList 초기화
    openList = []
    closedList = []
    openIndexList = []
    closedIndexList = []

    #교통 자원 및 노선 리스트 초기화
    mobility_type = []
    line_type = []

    # closedList에 시작 노드 추가
    startStructure = {'G' : 0, 'H': 0, 'ParentNode' : 0, 'id' : start}
    closedList.append(startStructure)
    closedIndexList.append(start)
    mobility_type.append(0)
    line_type.append('')

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
        for w in range(1,len(currentVector) + 1):
            adjacentIndex = w - 1
            adjacency = currentVector[adjacentIndex]
            if adjacency != 0 and adjacentIndex not in closedIndexList:
                #인접한 노드에 대한 구조 리스트 생성
                newStructureList = nodeStructure(node, AMatrix, end, adjacentIndex, currentIndex, parentStructure)
                #newStructureList에서 이용 가능한 교통 자원만 뽑아내기
                nList = []
                for s in newStructureList:
                    if s['F'] != math.inf:
                        nList.append(s)
                #인접한 노드가 openList의 기존에 있는 값보다 작은 F값을 가지는 경우 대체 (노드 인덱스와 교통 자원의 종류 확인)
                if adjacentIndex in openIndexList:
                    for n in openList:
                        if n['id'] == adjacentIndex:
                            originalIndex = openList.index(n)
                            #교통 자원 종류와 F값, 노선 종류 비교
                            for k in nList:
                                if k['type'] == n['type']:
                                    if k['line'] == n['line']:
                                        if k['F'] < n['F']:
                                            openList.remove(n)
                                            del openIndexList[originalIndex]
                                            openList.append(k)
                                            openIndexList.append(adjacentIndex)
                else:
                    for n in nList:
                        openList.append(n)
                        openIndexList.append(adjacentIndex)
        #openList에서 가장 작은 F값을 가지는 노드를 closedList에 추가
        #초기 값
        minFValue = math.inf
        #최소 F값 구하기
        for n in openList:
            if n['F'] < minFValue:
                minFValue = n['F']
        numOpen = len(openList)
        #최소 F값을 가지는 노드 closedList에 추가
        for i in range(0, numOpen):
            n = openList[i]
            if n['F'] == minFValue:
                closedList.append(n)
                #최소 F값을 가지는 노드의 id, type, line
                minimalIndex = n['id']
                closedIndexList.append(minimalIndex)
                minimalType = delimiters.index(n['type'])
                minimalLine = n['line']
                #현재 노드 설정
                currentNode = node[minimalIndex]
                currentIndex = minimalIndex
                #교통 자원의 종류
                #버스에서 다른 교통수단으로 바꾸는 경우
                if (len(mobility_type) > 0):
                    if (mobility_type[-1] == 4):
                        if (minimalType != mobility_type[-1]):
                          shouldWait = True
                mobility_type.append(minimalType)
                line_type.append(minimalLine)
                #현재 인접 벡터 설정
                currentVector = AMatrix[currentIndex]
                #부모 노드 설정
                parentStructure = n
                #openList에 있던 것 제거
                del openIndexList[i]
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
    #return [closedList, closedIndexList, closed_type_list, line_type]
    return [closedList, closedIndexList, mobility_type, line_type]

#최단 경로를 표출
#0-최단 경로의 노드 구조
#1-최단 경로의 노드 인덱스
#2-각 스텝을 이동하는 데 사용되는 교통 자원
#3-각 스텝을 이동하는 데 사용되는 버스 노선 (없으면 '')
#4-이동하는 데 드는 총 비용 (단위: 시간 [시])
#5-스텝 별 이동 비용
def describeShortestPath(node, AMatrix, start, end):
    closedListList = aStar(node, AMatrix, start, end)
    closedList = closedListList[0]
    closedList.remove({'state' : 'finished'})

    shortestPath = []
    shortestPathId = []
    startNode = closedList[0]
    startNodeId = startNode['id']
    closedList.remove(startNode)
    #서로 다른 경로 세트를 담을 dictionary
    fSet = dict()
    i = 0
    parent = start

    #Parent Node에 따라 경로 분류
    for n in closedList:
        if n['ParentNode'] == parent:
            shortestPath.append(n)
            shortestPathId.append(n['id'])
            fSet[str(i)] = n['H']
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
            while parent != start:
                for c in closedList:
                    if c['id'] == parent:
                        shortestPath.append(c)
                        shortestPathId.append(c['id'])
                        parentNode = c
                        parent = parentNode['ParentNode']
                        break
            shortestPath.reverse()
            shortestPathId.reverse()
            #역추적 완료 후 추가
            shortestPath.append(n)
            shortestPathId.append(n['id'])
            fSet[str(i)] = n['H']
            fSet[str(i) + 'Path'] = shortestPath
            fSet[str(i) + 'Id'] = shortestPathId
            parent = n['id']

    #가장 작은 H값을 가지는 '하나의' 경로 호출
    minPathValue = math.inf
    result = ["Not found", "Not found"]
    for k in range(0, i + 1):
        keyI = str(k)
        if fSet[keyI] < minPathValue:
            minPathValue = fSet[keyI]
    for k in range(0, i + 1):
        keyI = str(k)
        if fSet[keyI] == minPathValue:
            result = [[startNode] + fSet[keyI + 'Path'], [startNodeId] + fSet[keyI + 'Id']]
    
    #result와 closedList를 비교하면서 이용하는 교통 자원 파악
    #스텝 별 이동 비용 계산
    type_result = []
    line_result = []
    expense_list = []
    l_result = result[0]
    del l_result[0]
    for n in l_result:
        type_result.append(delimiters.index(n['type']))
        line_result.append(n['line'])
        expense_list.append(n['interval'])
    result.append(type_result)
    result.append(line_result)

    #이동 비용 계산
    expense = sum(expense_list)
    result.append(expense)

    result.append(expense_list)

    return result

data1 = sys.argv[1]
data2 = sys.argv[2]
data1 = int(data1)
data2 = int(data2)
path = describeShortestPath(data, AMatrix, data1, data2)
print(json.dumps(path))
# print("Path: " + str(path[1]))
# print("Mobility type: " + str(path[2]))
# print("Line type: " + str(path[3]))
# print("Expense: " + str(path[4] * 60) + " min")
# print("Expense list: " + str(path[5]))