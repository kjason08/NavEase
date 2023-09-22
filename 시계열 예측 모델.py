import os
import pandas as pd
import pandas_datareader.data as pdr

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

import matplotlib.pyplot as plt
import matplotlib

import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

import seaborn as sns
plt.style.use('seaborn-whitegrid')
import itertools
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import joblib
from pmdarima import auto_arima

input_folder = "C:\\Users\\kjaso\\Documents\\KAIST\\2023 가을\\기술을 통한 사회적 혁신 실험 4\\NavEase\\2차가공104bus데이터0803~0817"
output_folder = "C:\\Users\\kjaso\\Documents\\KAIST\\2023 가을\\기술을 통한 사회적 혁신 실험 4\\NavEase\\models104bus"

# 입력 폴더 내의 엑셀 파일 목록 가져오기
input_files = [f for f in os.listdir(input_folder) if f.endswith('.xlsx')]


# 디렉토리 내의 모델 저장 경로 설정
model_directory = output_folder
os.makedirs(model_directory, exist_ok=True)


# 1열의 데이터 추출
for j, input_file in enumerate(input_files):
    # 엑셀 파일 읽기
    file_path = os.path.join(input_folder, input_file)
    print(f"Processing {excel_file}...")

    #엑셀파일 읽기
    data = pd.read_excel(file_path)
    rows, cols = data.shape
    
    for i in range(1,rows-1):
        time_series = np.array(data.iloc[1:, i].values)

        # ARIMA 모델 생성 및 훈련
        model = auto_arima(time_series, seasonal=False, stepwise=True, suppress_warnings=True)

        # 모델 저장
        model_filename = os.path.join(model_directory, f'{excel_file}_{col}_model.pkl')
        joblib.dump(model, model_filename)

        # 다음 값을 예측
        next_prediction = model.predict(n_periods=1)
        print(f"Next Prediction for {col}: {next_prediction[0]}")

