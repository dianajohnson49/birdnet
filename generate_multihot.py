import os
import pandas as pd
from pydub import AudioSegment
from tqdm import tqdm
from collections import defaultdict

# =========================
# CONFIG
# =========================
CSV_PATH = "annotation_files/combined_annotations.csv"

# Updated to include the "all_birds" subdirectory
SUBDIR_NAME = "all_birds"
OUTPUT_AUDIO_DIR = os.path.join("training", "clips", SUBDIR_NAME)
OUTPUT_CSV_PATH = "training/annotations_multilabel.csv"

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

# =========================
# GROUP BY SOURCE + TIME WINDOW
# =========================
groups = defaultdict(list)

for _, row in df.iterrows():
    file_path = row["Begin Path"]
    start = float(row["File Offset (s)"])
    species = row["Common Name"]
    window_start = int(round(start / 3) * 3)
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

        if len(clip) < CLIP_DURATION_MS:
            continue

        # Generate filename
        base = os.path.splitext(os.path.basename(file_path))[0]
        clip_name = f"{base}_{window_start}s_{window_start+3}s.wav"
        out_path = os.path.join(OUTPUT_AUDIO_DIR, clip_name)

        clip.export(out_path, format="wav")

        # Format labels as comma-separated (per your example)
        unique_species = sorted(set(species_list))
        label_str = ", ".join(unique_species)

        # UPDATED RECORD FORMAT
        records.append({
            "audio_subdir": SUBDIR_NAME,
            "file": clip_name, # Just the filename, not the full path
            "labels": label_str
        })

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# =========================
# SAVE ANNOTATIONS CSV
# =========================
# Reorder columns to match the target format exactly
out_df = pd.DataFrame(records)
out_df = out_df[["audio_subdir", "file", "labels"]]
out_df.to_csv(OUTPUT_CSV_PATH, index=False)

print("Done.")
print(f"Clips saved to: {OUTPUT_AUDIO_DIR}")
print(f"Annotations saved to: {OUTPUT_CSV_PATH}")