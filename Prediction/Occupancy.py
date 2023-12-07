#XGBoost에 기반한 차량 내 재차 인원 예측 모델
import pandas as pd
import xgboost as xgb
import pickle
import sys, os
from datetime import datetime
#Astar 폴더 불러오기
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("Astar/getWeatherInfo"))))
from Astar import getWeatherInfo

getW = getWeatherInfo.Weather()

class Occupancy:
    from Astar import getWeatherInfo
    def __init__(self):
        self.model_path = "Prediction/Model/"

    #차량 내 재차 인원 예측
    def getNumInBus(self, bus_stop, bus_number):
        Week = datetime.today().weekday()
        #오늘 날짜 불러오기
        today = str(datetime.today())
        todayList = today.split(" ")
        dateList = todayList[0].split("-")
        timeList = todayList[1].split(":")
        date = ""
        for d in dateList:
            date += d
        time = timeList[0] + timeList[1]
        Temperature = getW.getTemp(date, time)
        Rain = getW.getRain(date, time)
        Snow = getW.getSnow(date, time)
        PM10 = getW.getPM10()
        PM2_5 = getW.getPM25()
        #코로나 여부 판단
        if int(dateList[0]) >= 2020:
            if int(dateList[0]) == 2023 and int(dateList[1]) > 4:
                COVID19 = 0
            else:
                COVID19 = 1
        else:
            COVID19 = 0
        input = {"Week": Week, "Temperature": Temperature, "Rain": Rain, "Snow": Snow, "PM10": PM10, "PM2.5": PM2_5, 
         "COVID19": COVID19, "Time": int(timeList[0])}
        x_input = pd.DataFrame(input, index=[0])
        #예측
        file_name = bus_stop + '_' + bus_number + '.pkl'
        file_path = self.model_path + file_name
        xgb_model = pickle.load(open(file_path, 'rb'))
        prediction = xgb_model.predict(x_input)

        return prediction[0]


OC = Occupancy()
print(OC.getNumInBus('42750', '105'))