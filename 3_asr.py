import glob
import os.path

import whisper
from tqdm import tqdm
from whisper.tokenizer import get_tokenizer
from pydub import AudioSegment

input_dir = "data/audio"
output_dir = "data/wavs"

os.makedirs(output_dir, exist_ok=True)

model = whisper.load_model("small", device="cuda")
tokenizer = get_tokenizer(multilingual=True)
available_tokens_idx = [
    i
    for i in range(tokenizer.eot)
    if all(
        c
        in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя?!:-().,"
        for c in tokenizer.decode([i]).strip()
    )
]

disabled_tokens_idx = []

for i in range(tokenizer.eot):
    if i not in available_tokens_idx:
        disabled_tokens_idx.append(i)


def transcribe(audio_file):
    return model.transcribe(
        audio_file, language="ru", suppress_tokens=[-1] + disabled_tokens_idx
    )


for file in tqdm(glob.glob(os.path.join(input_dir, "*.wav"))):
    segments = transcribe(file)["segments"]

    audio = AudioSegment.from_wav(file)

    for i, segment in enumerate(segments):
        text = segment["text"].strip()
        start, end = segment["start"], segment["end"]

        audio_segment = audio[start * 1000 : end * 1000]

        output_file = os.path.join(
            output_dir, f"{os.path.splitext(os.path.basename(file))[0]}_{i}.wav"
        )
        audio_segment.export(output_file, format="wav")

        with open(
            os.path.join(
                output_dir, f"{os.path.splitext(os.path.basename(file))[0]}_{i}.txt"
            ),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(text)
