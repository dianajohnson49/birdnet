import os
import pandas as pd
from pydub import AudioSegment
from tqdm import tqdm
from collections import defaultdict


# =========================
# CONFIG
# =========================
CSV_PATH = "annotation_files/combined_annotations.csv"

OUTPUT_AUDIO_DIR = "training/clips"
OUTPUT_CSV_PATH = "training/annotations_multilabel.csv"

CLIP_DURATION_MS = 3000  # 3 seconds

os.makedirs(OUTPUT_AUDIO_DIR, exist_ok=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(CSV_PATH)
df["Begin Path"] = df["Begin Path"].str.replace('\\', '/', regex=False)
# Normalize paths (important for Windows paths like E:\...)

# =========================
# CACHE AUDIO FILES
# =========================
audio_cache = {}

def load_audio(path):
    if path not in audio_cache:
        audio_cache[path] = AudioSegment.from_wav(path)
    return audio_cache[path]

# =========================
# GROUP BY SOURCE + TIME WINDOW
# =========================
# We group into 3-second windows:
# key = (file, window_start)
groups = defaultdict(list)

for _, row in df.iterrows():
    file_path = row["Begin Path"]
    start = float(row["File Offset (s)"])
    end = float(row["Delta Time (s)"])
    species = row["Species Code"]

    # align to 3-second window
    window_start = int(start // 3 * 3)

    groups[(file_path, window_start)].append(species)

# =========================
# CREATE CLIPS + MULTI-LABELS
# =========================
records = []

for (file_path, window_start), species_list in tqdm(groups.items()):
    try:
        audio = load_audio(file_path)

        start_ms = window_start * 1000
        end_ms = start_ms + CLIP_DURATION_MS

        clip = audio[start_ms:end_ms]

        # skip short clips
        if len(clip) < CLIP_DURATION_MS:
            continue

        # generate filename
        base = os.path.splitext(os.path.basename(file_path))[0]
        clip_name = f"{base}_{window_start}s_{window_start+3}s.wav"
        out_path = os.path.join(OUTPUT_AUDIO_DIR, clip_name)

        clip.export(out_path, format="wav")

        # store multi-label info (semicolon-separated)
        unique_species = sorted(set(species_list))
        label_str = ";".join(unique_species)

        records.append({
            "file": out_path,
            "start_time": window_start,
            "end_time": window_start + 3,
            "labels": label_str
        })

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# =========================
# SAVE ANNOTATIONS CSV
# =========================
out_df = pd.DataFrame(records)
out_df.to_csv(OUTPUT_CSV_PATH, index=False)

print("Done.")
print(f"Clips saved to: {OUTPUT_AUDIO_DIR}")
print(f"Annotations saved to: {OUTPUT_CSV_PATH}")