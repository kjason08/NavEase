import requests

#기온, 1시간 강수량에 대한 초단기 실황 및 적설량에 대한 1시간 단기예보, 미세먼지 및 초미세먼지 농도
#API: 기상청 단기예보 조회서비스, 한국환경공단 에어코리아 대기오염정보
class Weather:
    def __init__(self):
        self.content_list_short = []
        self.content_list_normal = []
        self.content_list_PM = []
    
    #초단기 실황 호출 데이터 정리: date: YYYYMMDD, time: hhmm
    def loadShortContent(self, date, time):
        url = url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
        serviceKey = '0QU3UHbIp56JlQiN2tbMykrBVxb%2F2%2F1lp3QpUwbFtlWDb9r9wwy9sIh4RLOlFli78fMdsiTH22N0Xr%2BvakQQ6w%3D%3D'
        serviceKey_decode = requests.utils.unquote(serviceKey)
        #대전광역시 유성구 기준
        params ={'serviceKey' : serviceKey_decode, 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'XML', 
                 'base_date' : date, 'base_time' : time, 'nx' : '67', 'ny' : '101' }
        response = requests.get(url, params=params)
        response_str = str(response.content.decode())
        self.content_list_short = response_str.split(">")

    #기온 초단기 실황
    def getTemp(self, date, time):
        self.loadShortContent(date, time)
        for str in self.content_list_short:
            if 'T1H' in str:
                index = self.content_list_short.index(str)
                obsrValue = float(self.content_list_short[index + 6].split("<")[0])
                break

        return obsrValue
    
    #1시간 강수량 초단기 실황
    def getRain(self, date, time):
        self.loadShortContent(date, time)
        for str in self.content_list_short:
            if 'RN1' in str:
                index = self.content_list_short.index(str)
                obsrValue = float(self.content_list_short[index + 6].split("<")[0])
                break

        return obsrValue
    
    #단기예보 호출 데이터 정리: date: YYYYMMDD, time: hhmm
    def loadNormalContent(self, date, time):
        url = url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
        serviceKey = '0QU3UHbIp56JlQiN2tbMykrBVxb%2F2%2F1lp3QpUwbFtlWDb9r9wwy9sIh4RLOlFli78fMdsiTH22N0Xr%2BvakQQ6w%3D%3D'
        serviceKey_decode = requests.utils.unquote(serviceKey)
        #대전광역시 유성구 기준
        params ={'serviceKey' : serviceKey_decode, 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'XML', 
                 'base_date' : date, 'base_time' : time, 'nx' : '67', 'ny' : '101' }
        response = requests.get(url, params=params)
        response_str = str(response.content.decode())
        self.content_list_normal = response_str.split(">")

    #1시간 신적설
    def getSnow(self, date, time):
        self.loadNormalContent(date, time)
        for str in self.content_list_normal:
            if 'SNO' in str:
                index = self.content_list_normal.index(str)
                obsrStr = self.content_list_normal[index + 6].split("<")[0]
                if '없음' in obsrStr:
                    obsrValue = float(0)
                else:
                    obsrValue = float(obsrStr)
                break
            else:
                obsrValue = float(0)

        return obsrValue
    
    #미세먼지 농도 호출
    def loadPMContent(self):
        url = url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
        serviceKey = '0QU3UHbIp56JlQiN2tbMykrBVxb%2F2%2F1lp3QpUwbFtlWDb9r9wwy9sIh4RLOlFli78fMdsiTH22N0Xr%2BvakQQ6w%3D%3D'
        serviceKey_decode = requests.utils.unquote(serviceKey)
        #대전광역시 유성구 기준
        params ={'serviceKey' : serviceKey_decode, 'returnType' : 'xml', 'numOfRows' : '100', 'pageNo' : '1', 
                 'stationName' : '종로구', 'dataTerm' : 'DAILY', 'ver' : '1.0' }
        response = requests.get(url, params=params)
        response_str = str(response.content.decode())
        self.content_list_PM = response_str.split(">")
    
    #PM10
    def getPM10(self):
        self.loadPMContent()
        for str in self.content_list_PM:
            if '</pm10Value' in str:
                str_list = str.split('<')
                return float(str_list[0])
    #PM2.5
    def getPM25(self):
        self.loadPMContent()
        for str in self.content_list_PM:
            if '</pm25Value' in str:
                str_list = str.split('<')
                return float(str_list[0])



    


