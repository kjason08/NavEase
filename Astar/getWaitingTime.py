import requests

#정류장 ARS-ID에 기반하여, 대전광역시 버스 대기 시간을 얻어오는 class
#API: 대전광역시-정류소별 도착정보 조회 서비스
class WaitingTime:
    def __init__(self):
        self.content_list = []
        self.itemCnt = 0
        self.line_list = []
        self.min_list = []
        self.sec_list = []
    #API를 통해 호출한 데이터 정리
    def setContent(self, arsId):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
        url = 'http://openapitraffic.daejeon.go.kr/api/rest/arrive/getArrInfoByUid'
        serviceKey = '0QU3UHbIp56JlQiN2tbMykrBVxb%2F2%2F1lp3QpUwbFtlWDb9r9wwy9sIh4RLOlFli78fMdsiTH22N0Xr%2BvakQQ6w%3D%3D'
        serviceKey_decode = requests.utils.unquote(serviceKey)
        params = {'serviceKey' : serviceKey_decode, 'arsId' : arsId}
        response = requests.get(url, params=params, headers=headers)

        byte_content = response.content
        content = byte_content.decode()
        self.content_list = content.split(">")

    #호출된 item 개수
    def getItemCount(self, arsId):
        self.setContent(arsId)
        for str in self.content_list:
            if '</itemCnt' in str:
                str_list = str.split("<")
                self.itemCnt = int(str_list[0])
                break
        return self.itemCnt
    
    #호출된 버스 노선 목록
    def getLineList(self, arsId):
        self.setContent(arsId)
        for str in self.content_list:
            if '</ROUTE_NO' in str:
                str_list = str.split("<")
                self.line_list.append(str_list[0])

        return self.line_list
    
    #호출된 버스 대기 시간 목록 (분 단위)
    def getMinDict(self, arsId):
        self.setContent(arsId)
        for str in self.content_list:
            if '</EXTIME_MIN' in str:
                str_list = str.split("<")
                self.min_list.append(str_list[0])

        return self.min_list
    
    #호출된 버스 대기 시간 목록 (초 단위)
    def getSecDict(self, arsId):
        self.setContent(arsId)
        for str in self.content_list:
            if '</EXTIME_SEC' in str:
                str_list = str.split("<")
                self.sec_list.append(str_list[0])

        return self.sec_list
    

#예제 코드
wt = WaitingTime()
print(wt.getLineList('42830'))