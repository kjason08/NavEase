import numpy as np
import math

#카이스트~신세계 백화점까지의 노드 데이터
#위도, 경도 데이터
data_SSG = [[36.36554700560022, 127.3639420558333],[36.365067517398224, 127.36287990106341],[36.36741561452646, 127.3673073135175],
            [36.36551442734556, 127.36963057553203],[36.37460622627934, 127.37938819412496],[36.37115352354895, 127.37933897456136],
            [36.37435862650956, 127.38227635027323]]
arr_SSG = np.array(data_SSG)
#인접 여부 데이터
isAdjacent_SSG = [[0,1,1,0,0,0,0],[1,0,0,0,0,0,0],[1,0,0,1,1,0,0],[0,0,1,0,0,1,0],
                  [0,0,0,0,0,1,1],[0,0,0,1,1,0,0],[0,0,0,0,1,0,0]]

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
                adjacencyRow.append(getDistance(location[indexI][0], location[indexI][1], 
                                                location[indexJ][0], location[indexJ][1]))
            else:
                adjacencyRow.append(math.inf)
            indexJ += 1
        A.append(adjacencyRow)
        indexI += 1
    return A

#Heuristic matrix 생성
def heuristic(node, goal):
    goalNode = node[goal]
    H = []
    for n in node:
        H.append(getDistance(n[0], n[1], goalNode[0], goalNode[1]))
    
    return H

# A* 알고리즘
def aStar(node, isAdjacency, start, end):
    # startNode와 endNode 초기화 (현재 기준은 인덱스)
    graph = getWDAdjacency(node, isAdjacency)
    startNode = graph[start]
    endNode = graph[end]

    #nextList, holdList 초기화
    # : [3, 2, 1] 식으로 경로 표시
    nextList = []
    holdList = []

    #Heuristic matrix 생성
    H = heuristic(node, end)

    # openList에 시작 노드 추가
    nextList.append(start)

    # 현재 노드 지정
    currentNode = graph[nextList[0]]
    currentIndex = graph.index(graph[nextList[0]])

    # endNode를 찾을 때까지 실행
    while currentIndex != end:
        currentG = np.array(currentNode)
        npH = np.array(H)
        currentF = currentG + npH
        currentF = currentF.tolist()
        currentf = min(currentF)

        # 나머지 후보 holdList에 추가
        for h in currentF:
            if h != currentf and h != math.inf:
                holdList.append([currentF.index(h)])
        print(holdList)
        fIndex = currentF.index(currentf)
        for item in holdList:
            itemF = H[item[0]]
            lenItem = len(item)
            i = 0
            checkListChanged = 0
            # holdList에 있는 경로 f값 계산
            while i != lenItem - 1:
                itemF += graph[item[i]][item[i + 1]]
                i += 1
            # holdList에 있는 인덱스가 더 적은 f값을 가지면
            # nextList로 옮기기
            if itemF < currentf:
                holdList.append(nextList)
                holdList.remove(item)
                nextList = item
                currentNode = graph[nextList[0]]
                currentIndex = graph.index(graph[nextList[0]])
                checkListChanged = 1
                currentG = np.array(currentNode)
                currentF = currentG + npH
                currentF = currentF.tolist()
                currentf = min(currentF)

        if checkListChanged == 0:
            nextList.insert(0, fIndex)
            currentNode = graph[nextList[0]]
            currentIndex = graph.index(graph[nextList[0]])
    
    return nextList

print(aStar(data_SSG, isAdjacent_SSG, 0, 6))




            