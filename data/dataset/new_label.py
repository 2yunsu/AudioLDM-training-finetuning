import pandas as pd

# 기존 CSV 파일 경로
input_csv_path = 'VGG-Foley-Sound_dataset.csv'
# 새로운 CSV 파일 저장 경로
train_csv_path = 'train_data.csv'
test_csv_path = 'test_data.csv'

# CSV 파일 읽기
df = pd.read_csv(input_csv_path)

# 'train/test split' 열에 따라 데이터 분리
train_df = df[df['train/test split'] == 'train']
test_df = df[df['train/test split'] == 'test']

# 새로운 데이터프레임 생성
train_df = pd.DataFrame({
    'Index': range(1, len(train_df) + 1),            # 1부터 시작하는 인덱스 번호
    'YouTube ID': train_df['YouTube ID'],            # 기존 CSV 파일의 1열
    'start_time': train_df['start seconds'],         # 기존 CSV 파일의 2열
    'predicted_materials': train_df['predicted_materials']  # 기존 CSV 파일의 6열
})

test_df = pd.DataFrame({
    'Index': range(1, len(test_df) + 1),            # 1부터 시작하는 인덱스 번호
    'YouTube ID': test_df['YouTube ID'],            # 기존 CSV 파일의 1열
    'start_time': test_df['start seconds'],         # 기존 CSV 파일의 2열
    'predicted_materials': test_df['predicted_materials']  # 기존 CSV 파일의 6열
})

# CSV 파일로 저장
train_df.to_csv(train_csv_path, index=False)
test_df.to_csv(test_csv_path, index=False)

print(f"Train CSV 파일이 생성되었습니다: {train_csv_path}")
print(f"Test CSV 파일이 생성되었습니다: {test_csv_path}")
