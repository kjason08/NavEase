import os
import pandas as pd
import numpy as np
from pmdarima import auto_arima

input_folder = "C:\\Users\\kjaso\\Documents\\KAIST\\2023 가을\\기술을 통한 사회적 혁신 실험 4\\NavEase\\2차가공104bus데이터0803~0817"
output_folder = "C:\\Users\\kjaso\\Documents\\KAIST\\2023 가을\\기술을 통한 사회적 혁신 실험 4\\NavEase\\models104bus"

# 입력 폴더 내의 엑셀 파일 목록 가져오기
input_files = [f for f in os.listdir(input_folder) if f.endswith('.xlsx')]


predictions = []
# 1열의 데이터 추출
for j, input_file in enumerate(input_files):
    # 엑셀 파일 읽기
    file_path = os.path.join(input_folder, input_file)
    print(file_path)
    data = pd.read_excel(file_path)
    rows, cols = data.shape
    
    for i in range(1,rows-1):
        time_series = np.array(data.iloc[1:, i].values)

        # ARIMA 모델 생성 및 훈련
        model = auto_arima(time_series, seasonal=False, stepwise=True, suppress_warnings=True)
        
        # 다음 값을 예측
        next_prediction = model.predict(n_periods=1)
        predictions.append(next_prediction)


for i in range(0, rows*69):
    print(predictions[i][0])

