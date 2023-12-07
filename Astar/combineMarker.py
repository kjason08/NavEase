import json

def combineMarker():
    markers = []

    #카이스트 마커
    file_path_1 = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Markers/markers_KAIST.json"
    with open(file_path_1, 'r') as file:
        data_1 = json.load(file)
    markers.append(data_1)
    
    #어은동 마커 1
    file_path_2 = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Markers/markers_Eueun1.json"
    with open(file_path_2, 'r') as file:
        data_2 = json.load(file)
    markers.append(data_2)
    
    #어은동 마커 2
    file_path_3 = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Markers/markers_Eueun2.json"
    with open(file_path_3, 'r') as file:
        data_3 = json.load(file)
    markers.append(data_3)

    #궁동 마커
    file_path_4 = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Markers/markers_Gung.json"
    with open(file_path_4, 'r') as file:
        data_4 = json.load(file)
    markers.append(data_4)

    #도룡동 마커
    file_path_5 = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Markers/markers_Doryoung.json"
    with open(file_path_5, 'r') as file:
        data_5 = json.load(file)
    markers.append(data_5)

    #카이스트 마커2
    file_path_6 = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Markers/markers_KAIST2.json"
    with open(file_path_6, 'r') as file:
        data_6 = json.load(file)
    markers.append(data_6)

     #충남대학교 마커
    file_path_7 = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Markers/markers_CNU.json"
    with open(file_path_7, 'r') as file:
        data_7 = json.load(file)
    markers.append(data_7)
    
    #마커 인덱스 수정
    for node in data_2:
        node['number'] = node['number'] + len(markers[0])
    for node in data_3:
        node['number'] = node['number'] + len(markers[0] + markers[1])
    for node in data_4:
        node['number'] = node['number'] + len(markers[0] + markers[1] + markers[2])
    for node in data_5:
        node['number'] = node['number'] + len(markers[0] + markers[1] + markers[2] + markers[3])
    for node in data_6:
        node['number'] = node['number'] + len(markers[0] + markers[1] + markers[2] + markers[3] + markers[4])
    for node in data_7:
        node['number'] = node['number'] + len(markers[0] + markers[1] + markers[2] + markers[3] + markers[4] + markers[5])
    
    #마커 합치기
    data = data_1 + data_2 + data_3 + data_4 + data_5 + data_6 + data_7
    file_path = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Markers/markers.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file)

combineMarker()