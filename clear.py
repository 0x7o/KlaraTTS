import os
import wave
import contextlib


def get_duration(wav_file):
    with contextlib.closing(wave.open(wav_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def find_long_segments(segments_dir, min_duration=30):
    long_segments = []
    for file in os.listdir(segments_dir):
        if file.endswith(".wav"):
            wav_file = os.path.join(segments_dir, file)
            duration = get_duration(wav_file)
            if duration > min_duration:
                long_segments.append(file)
    return long_segments


segments_dir = "data/segments"
long_segments = find_long_segments(segments_dir)

if long_segments:
    print("Сегменты длиннее 20 секунд:")
    for segment in long_segments:
        print(segment)
else:
    print("Сегментов длиннее 20 секунд не найдено.")
