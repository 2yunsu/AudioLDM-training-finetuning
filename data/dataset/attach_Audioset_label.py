import pandas as pd

# CSV 파일 경로 설정
vgg_csv_path = './VGG-Foley-Sound_dataset.csv'
bridge_csv_path = './AStest_Audioset_bridge.csv'

# CSV 파일 읽기
vgg_df = pd.read_csv(vgg_csv_path)
bridge_df = pd.read_csv(bridge_csv_path)

# AStest_Audioset_bridge.csv의 'Astest_label'과 'Audioset_label'을 딕셔너리로 변환
label_mapping = dict(zip(bridge_df['Astest_label'], bridge_df['Audioset_label']))

# VGG-Foley-Sound_dataset.csv 파일에 대응하는 Audioset_label 열 추가
vgg_df['Audioset_label'] = vgg_df['label'].map(label_mapping)

# 결과를 새로운 CSV 파일로 저장
output_csv_path = 'VGG-Foley-Sound_dataset_with_Audioset_label.csv'
vgg_df.to_csv(output_csv_path, index=False)

print(f"변환이 완료되었습니다. 파일이 저장되었습니다: {output_csv_path}")
