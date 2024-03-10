import os
import wave
import contextlib


def get_duration(wav_file):
    with contextlib.closing(wave.open(wav_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def concatenate_wavs(wav1, wav2, output_wav):
    infiles = [wav1, wav2]
    outfile = output_wav
    data = []
    for infile in infiles:
        w = wave.open(infile, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()

    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()


def process_segments(wavs_dir, segments_dir):
    segments = {}
    for file in os.listdir(wavs_dir):
        if file.endswith(".txt"):
            with open(os.path.join(wavs_dir, file), 'r') as f:
                text = f.read().strip()
            if text.endswith(".") or text.endswith("?") or text.endswith("!"):
                # Whole sentence, leave as is
                wav_file = file[:-4] + ".wav"
                os.rename(os.path.join(wavs_dir, wav_file), os.path.join(segments_dir, wav_file))
                os.rename(os.path.join(wavs_dir, file), os.path.join(segments_dir, file))
            else:
                # Segment, add to dictionary for concatenation
                index = file[:-4].split("_")[0]
                if index not in segments:
                    segments[index] = []
                segments[index].append(file[:-4])

    for index, segment_ids in segments.items():
        segment_ids.sort(key=lambda x: int(x.split("_")[1]))
        output_wav = os.path.join(segments_dir, f"{index}.wav")
        output_txt = os.path.join(segments_dir, f"{index}.txt")

        wav1 = os.path.join(wavs_dir, segment_ids[0] + ".wav")
        full_text = ""
        for i in range(1, len(segment_ids)):
            wav2 = os.path.join(wavs_dir, segment_ids[i] + ".wav")
            concatenate_wavs(wav1, wav2, output_wav)
            wav1 = output_wav

            with open(os.path.join(wavs_dir, segment_ids[i] + ".txt"), 'r') as f:
                full_text += f.read().strip() + " "

            os.remove(os.path.join(wavs_dir, segment_ids[i] + ".wav"))
            os.remove(os.path.join(wavs_dir, segment_ids[i] + ".txt"))

        os.remove(os.path.join(wavs_dir, segment_ids[0] + ".wav"))
        os.remove(os.path.join(wavs_dir, segment_ids[0] + ".txt"))

        with open(output_txt, 'w') as f:
            f.write(full_text.strip())


wavs_dir = "data/wavs"
segments_dir = "data/segments"
os.makedirs(segments_dir, exist_ok=True)
process_segments(wavs_dir, segments_dir)
