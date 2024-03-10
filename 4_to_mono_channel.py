from pydub import AudioSegment
from glob import glob
from tqdm import tqdm

for file in tqdm(glob("data/wavs/*.wav")):
    sound = AudioSegment.from_wav(file)
    sound = sound.set_channels(1)
    sound.export(file, format="wav")
