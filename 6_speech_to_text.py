import glob
import whisper
import pandas as pd
from tqdm import tqdm
from whisper.tokenizer import get_tokenizer

model = whisper.load_model("large-v3", device="cuda")
tokenizer = get_tokenizer(multilingual=True)
number_tokens = [
    i
    for i in range(tokenizer.eot)
    if all(c in "0123456789" for c in tokenizer.decode([i]).strip())
]


def transcribe(audio_file):
    return model.transcribe(audio_file, language="ru", suppress_tokens=[-1] + number_tokens)["text"]


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
