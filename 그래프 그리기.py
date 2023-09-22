import pandas as pd
import matplotlib.pyplot as plt

# 엑셀 파일 경로
excel_file_path = "C:\\Users\\kjaso\\Documents\\KAIST\\2023 가을\\기술을 통한 사회적 혁신 실험 4\\NavEase\\2차가공121bus데이터0817~0905\\83.xlsx"

# 엑셀 파일을 데이터프레임으로 읽어오기
df = pd.read_excel(excel_file_path)

# 첫 번째 열의 데이터의 마지막 4자리만 추출하여 x축으로 사용
df.iloc[:, 0] = df.iloc[:, 0].astype(str).str[-4:]

# 그래프 그리기
plt.figure(figsize=(10, 6))  # 그래프 크기 설정

# 2열 이상의 데이터를 꺾은선 그래프로 그리기
for col in df.columns[1:]:
    plt.plot(df.iloc[:, 0], df[col], marker='o', label=col)

# 그래프 제목과 레이블 설정
plt.title('데이터 그래프')
plt.xlabel('X 축')
plt.ylabel('Y 축')

# 범례 표시
plt.legend()

# 그래프 보여주기
plt.tight_layout()
plt.show()



