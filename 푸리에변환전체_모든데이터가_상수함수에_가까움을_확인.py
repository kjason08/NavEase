import os
import numpy as np
import pandas as pd
from scipy.fft import fft

#엑셀 파일들이 들어있는 폴더 경로
input_folder = "C:\\Users\\kjaso\\Documents\\KAIST\\2023 가을\\기술을 통한 사회적 혁신 실험 4\\NavEase\\kjason08.github.io\\2차가공121bus데이터0817~0905"

#폴더 내의 모든 엑셀 파일의 이름을 가져옴
input_files = [f for f in os.listdir(input_folder) if f.endswith('.xlsx')]

#리스트를 스트링으로 변환하는 함수
def listToString(str_list):
    result = ""
    for s in str_list:
        result += str(s) + " "
    return result.strip()


#모든 엑셀 파일에 대해서 반복
for j, input_file in enumerate(input_files):
    file_path = os.path.join(input_folder, input_file)
    #엑셀 파일 불러오기
    df = pd.read_excel(file_path)
    
    #한 엑셀 파일내에서 반복
    for col in df.columns[1:]:
        data = df[col].values
        fft_result = np.round(abs(fft(data)))
        #푸리에 변환 결과를 리스트로 변환
        convert_list = fft_result.tolist()
        #푸리에 변환 결과를 큰 순서대로 정렬
        convert_list.sort(reverse=True)
        #만일 푸리에 변환 결과가 주파수가 0이 아닌 값이 주파수가 0인 값보다 크면 출력
        if fft_result[0] < convert_list[0]:
            print(file_path)
            print(np.round(abs(fft_result)))
        




      
    

            
        
 
