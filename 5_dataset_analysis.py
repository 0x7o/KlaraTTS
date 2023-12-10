import os
import librosa
from tqdm import tqdm

dataset_dir = "dataset/wavs"

total_length = 0
min_length = None
max_length = None
audio_count = 0

for filename in tqdm(os.listdir(dataset_dir)):
    if filename.endswith(".wav"):
        audio_file_path = os.path.join(dataset_dir, filename)
        audio, sr = librosa.load(audio_file_path, sr=None)

        audio_length = librosa.get_duration(y=audio, sr=sr)

        total_length += audio_length
        min_length = min(min_length, audio_length) if min_length is not None else audio_length
        max_length = max(max_length, audio_length) if max_length is not None else audio_length
        audio_count += 1

average_length = total_length / audio_count

print(f"Total length of dataset: {total_length / 3600:.2f} hours")
print(f"Average audio length: {average_length:.2f} seconds")
print(f"Minimum length: {min_length:.2f} seconds")
print(f"Maximum length: {max_length:.2f} seconds")
