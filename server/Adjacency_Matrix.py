import json

#인접행렬을 생성하는 클래스
class Adjacency:
    def __init__(self):
        self.marker_file_path = "Markers/markers.json"
        self.data = dict()
        self.AMatrix_num = []
        self.AMatrix = []
        self.AMatrix_intergrated = []
    
    #마커 로드
    def loadMarkers(self):
        with open(self.marker_file_path, 'r') as file:
            self.data = json.load(file)

    #인접 노드 인덱스 정보 입력
    def addAdjacency(self, AMatrix_num):
        self.AMatrix_num = AMatrix_num

    #통합 인접 정보
    def getIntergrated(self):
        self.AMatrix_intergrated = [[10],[10,2,7],[1,3],[2,4,7],[3,5],[4,6],[5,7],[3,1,8],[7,9,143],[8,123,146],
                                    [0,1,11],[10,12],[11,13],[12,126],[15,124,31,29],[14,22,16],[17,20,15,150],[16,18],[28,19,17],[18,20,24],
                                    [16,21,19],[20,24,22],[21,15,23],[22,24,25],[19,21,27,23],[31,23,26],[32,30,25,27],[33,26,28,24],[18,35,27],[14,141,30],
                                    [29,26,39],[14,25,38],[26,39,33,38],[27,32,34],[33,35,37],[28,36,34],[35,48,37],[34,36,42,46],[32,43,80],[32,30,40,41],
                                    [39,41],[40,39,58,142],[43,47,37],[38,32,42,44],[43,45,57],[44,47,55],[37,53,49],[53,42,45],[36,50,49],[48,46,52],
                                    [60,48,59,51],[68,52,50,56],[51,49,54],[46,47,54],[53,52,55],[45,54,56],[70,55,51,57],[58,71,44,56],[57,115,41],[50,119],
                                    [50,68,61,67],[60,62,66],[61,63,64],[62,80],[62,65],[66,82,64],[65,61,67],[66,60,69],[51,60,74,70],[67,79,83,75],
                                    [56,72,71,68],[57,115,70,80],[70,78,73],[72,74,76],[68,73,75],[74,69,76],[75,73,77],[76,78],[77,72,79],[78,84,81,69],
                                    [71,81,108],[117,80,79,91],[65,87,83],[82,69,86,84],[79,83,85],[84,90,86],[83,85,89,87],[82,88,86],[87,92,89],[88,86,93,94],
                                    [85,94,91,89],[118,108,81,90],[88,93,97],[89,94,96,92],[93,90,95],[94,102,96],[93,101,97,95],[92,98,96],[97,103,99],[98,100,105],
                                    [99,111,101],[100,96,102],[101,95,113,109],[98,104],[105,103],[104,99,106],[105,112,107],[106,114,110],[91,109],[102,108,110],
                                    [109,107,120,152],[100,113,112],[111,114,106],[111,102,114],[112,113,107],[58,71,116],[115,117],[81,116,118],[117,91,119],[118,120,59,41],
                                    [110,121,119],[120,119],[153],[9,124,141,125],[123,126],[123,137,126],[125,127,13],[126,128],[127,129],[130,140,128],
                                    [129,140,131],[130,132],[131,133],[132,140],[140,133,135],[134,136],[135,137],[125,138],[137,139],[138,140],
                                    [129,139],[123,142],[141,137,136],[9,8,144],[143,145],[144,148,147],[9,147],[145,146,150],[145,149],[148,150],
                                    [147,149,16], [110,153],[152,122]]
        return self.AMatrix_intergrated
        

    #인접해있는 노드의 인덱스 정보만을 가지고 인접 행렬 생성
    def getAdjacencyMatrix(self, AMatrix_num):
        self.addAdjacency(AMatrix_num)
        length = len(self.AMatrix_num)
        adjacency_matrix = []
        for i in range(0, length):
            Ad = self.AMatrix_num[i]
            A = []
            for j in range(0, length):
                if j in Ad:
                    A.append(1)
                else:
                    A.append(0)
            adjacency_matrix.append(A)
        return adjacency_matrix