import os
import pandas as pd
from pydub import AudioSegment
from tqdm import tqdm
from collections import defaultdict

# =========================
# CONFIG
# =========================
CSV_PATH = "bg_annotation_files/combined_annotations.csv"

OUTPUT_AUDIO_DIR = os.path.join("training", "audio", "Background")

CLIP_DURATION_MS = 3000  # 3 seconds

os.makedirs(OUTPUT_AUDIO_DIR, exist_ok=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(CSV_PATH)

target_folder = "2025 King Rail Project"

def make_relative(path):
    path = str(path).replace('\\', '/')
    if target_folder in path:
        relative_part = path.split(target_folder)[-1]
        return os.path.join(target_folder, relative_part.lstrip('/'))
    return path

df["Begin Path"] = df["Begin Path"].apply(make_relative)

# =========================
# CACHE AUDIO FILES
# =========================
audio_cache = {}

def load_audio(path):
    if path not in audio_cache:
        audio_cache[path] = AudioSegment.from_wav(path)
    return audio_cache[path]

seen = set()  # avoid duplicate windows

for _, row in tqdm(df.iterrows(), total=len(df)):
    try:
        file_path = row["Begin Path"]
        start = float(row["File Offset (s)"])

        # snap to 3-second window

        key = (file_path, start)
        if key in seen:
            continue
        seen.add(key)

        audio = load_audio(file_path)

        start_ms = start * 1000
        end_ms = start_ms + CLIP_DURATION_MS

        clip = audio[start_ms:end_ms]

        if len(clip) < CLIP_DURATION_MS:
            continue

        # filename
        base = os.path.splitext(os.path.basename(file_path))[0]
        clip_name = f"{base}_{start}s_{start+3}s.wav"

        out_path = os.path.join(OUTPUT_AUDIO_DIR, clip_name)

        clip.export(out_path, format="wav")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print("Done.")
print(f"Background clips saved to: {OUTPUT_AUDIO_DIR}")