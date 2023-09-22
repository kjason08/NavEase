import os
import numpy as np
import pandas as pd
from scipy.fft import fft

input_folder = "C:\\Users\\kjaso\\Documents\\KAIST\\2023 가을\\기술을 통한 사회적 혁신 실험 4\\NavEase\\kjason08.github.io\\2차가공121bus데이터0817~0905"

    
input_files = [f for f in os.listdir(input_folder) if f.endswith('.xlsx')]

#리스트를 스트링으로 변환하는 함수
def listToString(str_list):
    result = ""
    for s in str_list:
        result += str(s) + " "
    return result.strip()


#전체 데이터 담을 리스트 설정
fft_list = []
for j, input_file in enumerate(input_files):
    file_path = os.path.join(input_folder, input_file)
    #엑셀 파일 불러오기
    df = pd.read_excel(file_path)
    
    #한 엑셀 파일에 대한 데이터를 담을 리스트 설정
    list = []
    for col in df.columns[1:]:
        data = df[col].values
        fft_result = np.round(abs(fft(data)))
        convert_list = fft_result.tolist()
        convert_list.sort(reverse=True)
        if fft_result[0] < convert_list[0]:
            print(file_path)
            print(np.round(abs(fft_result)))
        list.append(np.round(abs(fft_result)))

    fft_list.append(list)


      
    

            
        
 
