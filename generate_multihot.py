import os
import pandas as pd
from pydub import AudioSegment
from tqdm import tqdm
from collections import defaultdict

# =========================
# CONFIG
# =========================
LABEL_CSV_PATH = "annotation_files/combined_annotations.csv"
BG_CSV_PATH = "bg_annotation_files/combined_annotations.csv"

OUTPUT_AUDIO_DIR = os.path.join("training", "audio")
BACKGROUND_DIR = os.path.join(OUTPUT_AUDIO_DIR, "Background")

OUTPUT_CSV_PATH = "training/annotations_multilabel.csv"

CLIP_DURATION_MS = 3000

os.makedirs(OUTPUT_AUDIO_DIR, exist_ok=True)
os.makedirs(BACKGROUND_DIR, exist_ok=True)

# =========================
# LOAD DATA
# =========================
df_labels = pd.read_csv(LABEL_CSV_PATH)
df_bg = pd.read_csv(BG_CSV_PATH)

target_folder = "2025 King Rail Project"

def make_relative(path):
    path = str(path).replace('\\', '/')
    if target_folder in path:
        relative_part = path.split(target_folder)[-1]
        return os.path.join(target_folder, relative_part.lstrip('/'))
    return path

df_labels["Begin Path"] = df_labels["Begin Path"].apply(make_relative)
df_bg["Begin Path"] = df_bg["Begin Path"].apply(make_relative)

# =========================
# AUDIO CACHE
# =========================
audio_cache = {}

def load_audio(path):
    if path not in audio_cache:
        audio_cache[path] = AudioSegment.from_wav(path)
    return audio_cache[path]

# =========================
# PART 1 — LABELED CLIPS
# =========================
groups = defaultdict(list)

for _, row in df_labels.iterrows():
    file_path = row["Begin Path"]
    start = float(row["File Offset (s)"])
    species = row["Common Name"]

    window_start = int(round(start / 3) * 3)
    groups[(file_path, window_start)].append(species)

records = []

print("Processing labeled clips...")

for (file_path, window_start), species_list in tqdm(groups.items()):
    try:
        audio = load_audio(file_path)

        start_ms = window_start * 1000
        end_ms = start_ms + CLIP_DURATION_MS

        clip = audio[start_ms:end_ms]

        if len(clip) < CLIP_DURATION_MS:
            continue

        base = os.path.splitext(os.path.basename(file_path))[0]

        clip_name = f"{base}_{window_start:.4f}s_{window_start+3:.4f}s.wav"
        out_path = os.path.join(OUTPUT_AUDIO_DIR, clip_name)

        clip.export(out_path, format="wav")

        label_str = ", ".join(sorted(set(species_list)))

        records.append({
            "audio_subdir": "audio",
            "file": clip_name,
            "labels": label_str
        })

    except Exception as e:
        print(f"Label error {file_path}: {e}")

# =========================
# PART 2 — BACKGROUND CLIPS
# =========================
background_records = []

for _, row in tqdm(df_bg.iterrows(), total=len(df_bg)):
    try:
        file_path = row["Begin Path"]
        start = round(float(row["File Offset (s)"]), 4)

        audio = load_audio(file_path)

        start_ms = int(start * 1000)
        end_ms = start_ms + CLIP_DURATION_MS

        clip = audio[start_ms:end_ms]

        if len(clip) < CLIP_DURATION_MS:
            continue

        base = os.path.splitext(os.path.basename(file_path))[0]

        clip_name = f"{base}_{start:.4f}s_{start+3:.4f}s.wav"

        out_path = os.path.join(BACKGROUND_DIR, clip_name)
        clip.export(out_path, format="wav")

        # ADD TO CSV
        background_records.append({
            "audio_subdir": "Background",
            "file": clip_name,
            "labels": ""
        })

    except Exception as e:
        print(f"Background error {file_path}: {e}")

# =========================
# SAVE CSV (LABELS ONLY)
# =========================
out_df = pd.DataFrame(records + background_records)
out_df = out_df[["audio_subdir", "file", "labels"]]
out_df.to_csv(OUTPUT_CSV_PATH, index=False)

print("Done.")
print(f"Labeled clips saved to: {OUTPUT_AUDIO_DIR}")
print(f"Background clips saved to: {BACKGROUND_DIR}")
print(f"Annotations saved to: {OUTPUT_CSV_PATH}")