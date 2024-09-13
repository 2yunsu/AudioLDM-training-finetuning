import os
import pandas as pd
# import youtube_dl
import ffmpeg
import yt_dlp as youtube_dl

# CSV 파일 경로 설정
csv_file_path = 'VGG-Foley-Sound_dataset.csv'
audio_output_dir = '/home/yslee/data/yslee/AudioLDM-training-finetuning/data/dataset/audioset'
video_output_dir = '/home/yslee/data/yslee/AudioLDM-training-finetuning/data/dataset/video'
cookie_file_path = 'cookies.txt'

# CSV 파일을 읽음
df = pd.read_csv(csv_file_path)

# 출력 디렉토리 생성
if not os.path.exists(video_output_dir):
    os.makedirs(video_output_dir)
if not os.path.exists(audio_output_dir):
    os.makedirs(audio_output_dir)

# 다운로드 및 트리밍 함수
def download_and_trim(video_id, start_time, video_output_dir, audio_output_dir):
    video_file_path = os.path.join(video_output_dir, f'{video_id}.mp4')
    audio_file_path = os.path.join(audio_output_dir, f'{video_id}.wav')
    
    trimmed_video_file_path = os.path.join(video_output_dir, f'{video_id}_trimmed.mp4')
    trimmed_audio_file_path = os.path.join(audio_output_dir, f'{video_id}_trimmed.wav')
    
    # 이미 트리밍된 파일이 존재하는지 확인
    if os.path.exists(trimmed_video_file_path) and os.path.exists(trimmed_audio_file_path):
        print(f'File {trimmed_video_file_path} and {trimmed_audio_file_path} already exist. Skipping download and trim.')
        return
    
    ydl_opts_video = {
        'format': 'bestvideo',
        'outtmpl': video_file_path,
        'cookiefile': cookie_file_path,  # 쿠키 파일 경로 추가
    }
    ydl_opts_audio = {
        'format': 'bestaudio',
        'outtmpl': audio_file_path,
        'cookiefile': cookie_file_path,  # 쿠키 파일 경로 추가
    }
    
    with youtube_dl.YoutubeDL(ydl_opts_video) as ydl:
        ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
    
    with youtube_dl.YoutubeDL(ydl_opts_audio) as ydl:
        ydl.download([f'https://www.youtube.com/watch?v={video_id}'])

    # ffmpeg를 사용하여 비디오 트리밍 (시작 시간부터 10초까지)
    ffmpeg.input(video_file_path, ss=start_time, t=10).output(trimmed_video_file_path).run()
    os.remove(video_file_path)

    # ffmpeg를 사용하여 오디오 트리밍 및 WAV 파일로 변환 (시작 시간부터 10초까지)
    ffmpeg.input(audio_file_path, ss=start_time, t=10).output(trimmed_audio_file_path).run()
    os.remove(audio_file_path)

# CSV 파일의 특정 행만 선택하여 다운로드 및 트리밍 수행
start_index = 0  # 시작 인덱스 (0부터 시작)
end_index = 40713    # 종료 인덱스 (포함되지 않음)

for index, row in df.iloc[start_index:end_index].iterrows():
    video_id = row[0]
    start_time = row[1]
    
    try:
        download_and_trim(video_id, start_time, video_output_dir, audio_output_dir)
    except Exception as e:
        print(f'Error for {video_id}: {e}')

print("다운로드 및 트리밍이 완료되었습니다.")