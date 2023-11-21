import json

def combineMarker():
    #봉명동 마커
    file_path_1 = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Markers/markers_Bongmyeong.json"
    with open(file_path_1, 'r') as file:
        data_1 = json.load(file)
    
    #어은동, 궁동, 도룡동 마커
    file_path_2 = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Markers/markers_EGD.json"
    with open(file_path_2, 'r') as file:
        data_2 = json.load(file)
    
    #타슈 정류장 마커
    file_path_3 = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Markers/markers_tashu.json"
    with open(file_path_3, 'r') as file:
        data_3 = json.load(file)

    #121번 마커
    #대덕대학 방면
    file_path_4 = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Markers/markers_121_D.json"
    with open(file_path_4, 'r') as file:
        data_4 = json.load(file)
    #탑립동 방면
    file_path_5 = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Markers/markers_121_U.json"
    with open(file_path_5, 'r') as file:
        data_5 = json.load(file)
    for node in data_5:
        node['customValue'] = node['customValue'] + 1
    
    #마커 인덱스 수정
    for node in data_2:
        node['number'] = node['number'] + len(data_1)
    for node in data_3:
        node['number'] = node['number'] + len(data_1 + data_2)
    for node in data_4:
        node['number'] = node['number'] + len(data_1 + data_2 + data_3)
    for node in data_5:
        node['number'] = node['number'] + len(data_1 + data_2 + data_3 + data_4)
    
    #마커 합치기
    data = data_1 + data_2 + data_3 + data_4 + data_5
    file_path = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Markers/markers.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file)

combineMarker()