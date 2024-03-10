import subprocess
import glob
import os


def video_to_wav(video_path, wav_path):
    subprocess.call(["ffmpeg", "-i", video_path, wav_path])


def main(video_dir, audio_dir):
    files = glob.glob(os.path.join(video_dir, "*.mp4"))
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    for idx, file in enumerate(files):
        print(idx, file)
        video_to_wav(file, os.path.join(audio_dir, f"{idx}.wav"))


if __name__ == "__main__":
    main(video_dir="videos", audio_dir="data/audio")
