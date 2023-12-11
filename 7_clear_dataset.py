import pandas as pd
import re

df = pd.read_csv("dataset/metadata.csv", sep="|")
new_data = []

for index, row in df.iterrows():
    file, text = row.values[0], row.values[1].lower()
    if not re.search("[a-z]", text) and re.search("[а-я]", text):
        new_data.append((file, text.strip(), text.strip()))

df = pd.DataFrame(new_data)
df.to_csv("dataset/cleaned_metadata.csv", index=False, sep="|")
