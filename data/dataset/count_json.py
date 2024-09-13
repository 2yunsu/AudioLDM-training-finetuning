import json

# JSON 파일 경로 설정
train_json_path = 'VGG-foley_train_label_2.json'
test_json_path = 'VGG-foley_test_label_2.json'

# JSON 파일 읽기 및 데이터 개수 확인 함수
def count_data_in_json(json_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        return len(data['data'])

# Train JSON 파일의 데이터 개수 출력
train_data_count = count_data_in_json(train_json_path)
print(f"Train 데이터 개수: {train_data_count}")

# Test JSON 파일의 데이터 개수 출력
test_data_count = count_data_in_json(test_json_path)
print(f"Test 데이터 개수: {test_data_count}")
