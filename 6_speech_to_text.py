import glob
import whisper
import pandas as pd
from tqdm import tqdm

model = whisper.load_model("small", device="cuda")


def transcribe(audio_file):
    return model.transcribe(audio_file, language="ru")["text"]


def main():
    data = []
    for audio_file in tqdm(glob.glob("dataset/wavs/*.wav")):
        text = transcribe(audio_file)
        print(f"{audio_file} -> {text}")
        data.append((audio_file.split("/")[-1].replace(".wav", ""), text, text))
    df = pd.DataFrame(data)
    df.to_csv("dataset/metadata.csv", index=False, sep="|")


if __name__ == "__main__":
    main()
