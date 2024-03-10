import glob
import os
from datasets import Dataset, Audio
from tqdm import tqdm

input_dir = "data/segments"
raw = {"audio": [], "text": []}

for file in tqdm(glob.glob(os.path.join(input_dir, "*.wav"))):
    with open(file.replace(".wav", ".txt"), "r") as f:
        text = f.read()
    raw["audio"].append(file)
    raw["text"].append(text)

dataset = Dataset.from_dict(raw).cast_column("audio", Audio())
dataset.push_to_hub("0x7o/klara-voice-merged")
