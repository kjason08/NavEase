import os
import pandas as pd
import numpy as np
from pmdarima import auto_arima

# 모델 저장과 불러오기를 위한 모듈
import joblib  

input_folder = "C:\\Users\\kjaso\\Documents\\KAIST\\2023 가을\\기술을 통한 사회적 혁신 실험 4\\NavEase\\2차가공121bus데이터0817~0905"
output_folder = "C:\\Users\\kjaso\\Documents\\KAIST\\2023 가을\\기술을 통한 사회적 혁신 실험 4\\NavEase\\models121bus"

# 입력 폴더 내의 엑셀 파일 목록 가져오기
input_files = [f for f in os.listdir(input_folder) if f.endswith('.xlsx')]

# ARIMA 모델 저장을 위한 폴더 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 1열의 데이터 추출
for j, input_file in enumerate(input_files):
    # 엑셀 파일 읽기
    file_path = os.path.join(input_folder, input_file)
    print(file_path)
    data = pd.read_excel(file_path)
    rows, cols = data.shape
    
    for i in range(1, rows-1):
        time_series = np.array(data.iloc[1:, i].values)

        # ARIMA 모델 생성 및 훈련
        model = auto_arima(time_series, seasonal=True, stepwise=True, suppress_warnings=True)
        
        # 모델 저장
        model_filename = os.path.splitext(input_file)[0] + f"_model_{i}.joblib"
        model_path = os.path.join(output_folder, model_filename)
        joblib.dump(model, model_path)

        # 다음 값을 예측
        next_prediction = model.predict(n_periods=7)
        print(next_prediction)
