import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from tqdm import tqdm

source_folder = 'data/audio'
destination_folder = 'dataset/waves'

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

min_silence_len = 500  # In milliseconds
silence_thresh = -40  # In dB, lowered for more sensitive silence detection
padding = 400  # In milliseconds, added to the beginning and end of each chunk

for filename in tqdm(os.listdir(source_folder)):
    if filename.endswith('.wav'):
        audio_number = os.path.splitext(filename)[0]

        audio_path = os.path.join(source_folder, filename)
        audio = AudioSegment.from_wav(audio_path)

        chunks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

        for i, chunk in enumerate(chunks):
            padded_chunk = AudioSegment.silent(duration=padding) + chunk + AudioSegment.silent(duration=padding)
            chunk_file_name = f'audio{audio_number}_chunk_{i}.wav'
            chunk_path = os.path.join(destination_folder, chunk_file_name)
            padded_chunk.export(chunk_path, format='wav')

        print(f'Successfully split {filename} into {len(chunks)} chunks.')

print('All audio files have been processed and saved in the dataset/waves folder.')
