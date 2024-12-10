import os
import json

# 폴더 경로 설정
folder_path = './Audio_datasets_hanwool'

# 파일 리스트 불러오기
files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

# JSON 데이터 생성
data = []
for file in files:
    wav = file  # 파일명만 저장
    caption = file.replace('.wav', '')  # 파일명에서 .wav 제거
    data.append({"wav": wav, "caption": caption})

# 최종 JSON 구조
json_data = {"data": data}

# JSON 파일 저장
with open('hanwool_train_label.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print("JSON 파일이 성공적으로 생성되었습니다.")