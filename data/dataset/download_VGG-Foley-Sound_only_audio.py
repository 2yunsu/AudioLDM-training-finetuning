import os
import pandas as pd
import ffmpeg
import yt_dlp as youtube_dl

# CSV 파일 경로 설정
csv_file_path = 'VGG-Foley-Sound_dataset.csv'
audio_output_dir = '/home/yslee/data/yslee/AudioLDM-training-finetuning/data/dataset/audioset_10s'
cookie_file_path = 'cookies.txt'

# CSV 파일을 읽음
df = pd.read_csv(csv_file_path)

# 출력 디렉토리 생성
if not os.path.exists(audio_output_dir):
    os.makedirs(audio_output_dir)

# 다운로드 및 트리밍 함수 (비디오 제외)
def download_and_trim_audio(video_id, start_time, audio_output_dir):
    audio_file_path = os.path.join(audio_output_dir, f'{video_id}.webm')  # 웹에서 다운로드하는 기본 오디오 형식은 주로 webm
    trimmed_audio_file_path = os.path.join(audio_output_dir, f'{video_id}.wav')

    # 이미 트리밍된 파일이 존재하는지 확인
    if os.path.exists(trimmed_audio_file_path):
        print(f'File {trimmed_audio_file_path} already exists. Skipping download and trim.')
        return

    ydl_opts_audio = {
        'format': 'bestaudio',
        'outtmpl': audio_file_path,
        'cookiefile': cookie_file_path,  # 쿠키 파일 경로 추가
    }
    
    # 오디오 다운로드
    with youtube_dl.YoutubeDL(ydl_opts_audio) as ydl:
        ydl.download([f'https://www.youtube.com/watch?v={video_id}'])

    # ffmpeg를 사용하여 오디오 트리밍 및 WAV 파일로 변환 (시작 시간부터 10초 동안 자르기)
    try:
        ffmpeg.input(audio_file_path, ss=start_time, t=10).output(trimmed_audio_file_path).run(overwrite_output=True)
        print(f"Trimmed audio saved as {trimmed_audio_file_path}")
    except Exception as e:
        print(f"Error while trimming audio for {video_id}: {e}")
    
    # 원본 오디오 파일 삭제
    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)

# CSV 파일의 특정 행만 선택하여 다운로드 및 트리밍 수행
start_index = 0  # 시작 인덱스 (0부터 시작)
end_index = 40713  # 종료 인덱스 (포함되지 않음)

for index, row in df.iloc[start_index:end_index].iterrows():

    video_id = row.iloc[0]  # 비디오 ID는 1열
    start_time = row.iloc[1]  # 시작 시간은 2열에 있음
    
    try:
        download_and_trim_audio(video_id, start_time, audio_output_dir)
    except Exception as e:
        print(f'Error for {video_id}: {e}')

print("다운로드 및 트리밍이 완료되었습니다.")
