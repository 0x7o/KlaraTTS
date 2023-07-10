import glob
import whisper
import pandas as pd
from tqdm import tqdm

model = whisper.load_model("small", device="cuda")


def transcribe(audio_file):
    return model.transcribe(audio_file, language="ru")["text"]


def main():
    data = []
    for audio_file in tqdm(glob.glob("dataset/waves/*.wav")):
        text = transcribe(audio_file)
        print(f"{audio_file} -> {text}")
        data.append((audio_file, text))
    df = pd.DataFrame(data, columns=["audio_file", "text"])
    df.to_csv("dataset/metadata.csv", index=False, sep="|")


if __name__ == "__main__":
    main()
