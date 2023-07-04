import os
from spleeter.separator import Separator


def separate_background_music(audio_path, output_path):
    # Create a separator with the 2stems model (vocals and accompaniments)
    separator = Separator("spleeter:2stems")

    # Separate audio into two stems: vocals and accompaniments
    separator.separate_to_file(audio_path, output_path)


def process_all_audio_files(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith(".wav"):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, filename)

            # Check if the output file already exists, and skip processing if it does
            if os.path.exists(output_file):
                print(f"Skipping {filename} as the output file already exists.")
                continue

            temp_output = os.path.join(output_directory, "temp")

            if not os.path.exists(temp_output):
                os.makedirs(temp_output)

            separate_background_music(input_file, temp_output)

            vocals_file = os.path.join(temp_output, filename.split('.')[0], "vocals.wav")

            os.rename(vocals_file, output_file)

            # Remove the accompaniment.wav file
            accompaniment_file = os.path.join(temp_output, filename.split('.')[0], "accompaniment.wav")
            os.remove(accompaniment_file)

            # Remove the directory after removing accompaniment.wav
            os.rmdir(os.path.join(temp_output, filename.split('.')[0]))


input_directory = 'data/audio'
output_directory = 'data/voice'

process_all_audio_files(input_directory, output_directory)