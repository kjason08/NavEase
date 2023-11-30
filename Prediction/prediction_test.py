import xgboost as xgb
from xgboost import plot_importance, plot_tree
import pandas as pds
import matplotlib.pyplot as plt
from matplotlib import rc
import pickle

#xgboost 모델 불러오기
file_path = "/Users/janghyeongjun/Documents/Projects/kjason08.github.io/Prediction/XGBoost_dataset.pkl"
xgb_model = pickle.load(open(file_path, 'rb'))

#데이터 입력
Week = 5
Temperature = 12.8
Rain = 0.1
Snow = 0.0
PM10 = 12
PM2_5 = 8
COVID19 = 0
Time = 4
BusStop = 44490
BusNumber = 5
input = {"Week": Week, "Temperature": Temperature, "Rain": Rain, "Snow": Snow, "PM10": PM10, "PM2.5": PM2_5, 
         "COVID19": COVID19, "Time": Time, "BusStop": BusStop, "BusNumber": BusNumber}
pdsInput = pds.DataFrame(input, index=[0])

#예측
prediction = xgb_model.predict(pdsInput)
bus_seat = 25
occupancy = (abs(prediction) / bus_seat) * 100
print(str(occupancy[0]) + " %")

#Tree 시각화
#plot_tree(xgb_model)
#plt.show()

