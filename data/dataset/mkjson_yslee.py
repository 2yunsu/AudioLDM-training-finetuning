import os
import pandas as pd
import json

# CSV 파일 경로 설정
vgg_csv_path = 'VGG-Foley-Sound_dataset_with_Audioset_label.csv'
audioset_folder = 'audioset'
train_output_json_path = 'VGG-foley_train_label_2.json'
test_output_json_path = 'VGG-foley_test_label_2.json'

# CSV 파일 읽기
vgg_df = pd.read_csv(vgg_csv_path)

# 출력 데이터 리스트
train_data_list = []
test_data_list = []

# audioset 폴더에서 .wav 파일 처리
for file_name in os.listdir(audioset_folder):
    if file_name.endswith('.wav'):
        file_path = os.path.join(audioset_folder, file_name)
        file_base_name = os.path.splitext(file_name)[0]  # 확장자를 제외한 파일명 (예: --0PQM4-hqg)

        # VGG CSV에서 파일명에 해당하는 행 찾기
        matched_row = vgg_df[vgg_df['YouTube ID'] == file_base_name]

        if not matched_row.empty:
            # CSV에서 필요한 데이터 추출
            audioset_label = matched_row['Audioset_label'].values[0]
            predicted_materials = matched_row['predicted_materials'].values[0]
            split = matched_row['train/test split'].values[0]  # Train/Test Split
            caption = matched_row['label'].values[0]  # Label (Caption)

            # JSON 데이터 구조 생성
            data_entry = {
                "wav": file_path,
                "labels": audioset_label,
                "caption": predicted_materials
            }

            # Train/Test 구분에 따라 데이터를 나눔
            if split == 'train':
                train_data_list.append(data_entry)
            elif split == 'test':
                test_data_list.append(data_entry)
        else:
            print(f"No matching entry found for {file_base_name} in the CSV file.")

# Train JSON 파일로 저장
train_output_data = {"data": train_data_list}
with open(train_output_json_path, 'w') as train_json_file:
    json.dump(train_output_data, train_json_file, indent=4)
print(f"Train JSON 파일이 생성되었습니다: {train_output_json_path}")

# Test JSON 파일로 저장
test_output_data = {"data": test_data_list}
with open(test_output_json_path, 'w') as test_json_file:
    json.dump(test_output_data, test_json_file, indent=4)
print(f"Test JSON 파일이 생성되었습니다: {test_output_json_path}")
