import pandas as pd
import xgboost as xgb
import pickle

#2023년 데이터 기반으로 예측 모델 테스트
#데이터 불러오기
data_path = "Dataset/test_dataset.csv"
data = pd.read_csv(data_path, encoding="cp949")
row_num = len(data)

#모델 불러오기
model_path = "Prediction/Model/"
error_list = []
y_list = []
p_list = []

for i in range(0, row_num):
    print(i + 1)
    x_test = data.iloc[i, 0:8]
    Week = data.iloc[i, 0]
    Temperature = data.iloc[i, 1]
    Rain = data.iloc[i, 2]
    Snow = data.iloc[i, 3]
    PM10 = data.iloc[i, 4]
    PM2_5 = data.iloc[i, 5]
    COVID19 = data.iloc[i, 6]
    Time = data.iloc[i, 7]
    input = {"Week": Week, "Temperature": Temperature, "Rain": Rain, "Snow": Snow, "PM10": PM10, "PM2.5": PM2_5, 
         "COVID19": COVID19, "Time": Time}
    x_input = pd.DataFrame(input, index=[0])
    y_test = data.iloc[i, 10]
    bus_stop = str(data.loc[i, 'BusStop'])
    bus_number = str(data.loc[i, 'BusNumber'])
    #해당하는 모델 찾기
    file_name = bus_stop + '_' + bus_number + '.pkl'
    file_path = model_path + file_name
    xgb_model = pickle.load(open(file_path, 'rb'))
    prediction = xgb_model.predict(x_input)
    absolute_error = abs(prediction - y_test)[0]
    error_list.append(absolute_error)

pf_dict = {"error": error_list}
pd_df = pd.DataFrame(pf_dict)
pd_df.to_csv('./Prediction/performance_test.csv')