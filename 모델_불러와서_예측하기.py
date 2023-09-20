import os
import joblib  # 모델 불러오기를 위한 모듈

# 모델이 저장된 폴더 경로
model_folder = "C:\\Users\\kjaso\\Documents\\KAIST\\2023 가을\\기술을 통한 사회적 혁신 실험 4\\NavEase\\models121bus"

# 불러올 모델 파일 이름
model_filename = "7_model_10.joblib"  # 모델 파일 이름을 적절하게 변경하세요

# 모델 파일 경로
model_path = os.path.join(model_folder, model_filename)

# 모델 불러오기
loaded_model = joblib.load(model_path)

# 다음 값을 예측
next_prediction = loaded_model.predict(n_periods=7)

print(f"Next prediction: {next_prediction}")
