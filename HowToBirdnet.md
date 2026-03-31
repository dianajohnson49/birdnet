## Date: 20250924

## Goal
Test and document use of BirdNET Analyzer CLI using the model not able to natively run on the GPU according to Mike Raymer
## Environment
- OS: Pop!_OS 22.04 LTS 
- Python Version: Python 3.11.0rc1
- BirdNET CLI Version: v2.2.0-2-gd31af6e
- BirdNET model version: 2.4
- Virtual Environment: venv

## Project Structure

BirdNet/
├── birdnet/             # ← virtual environment
├── BirdNET-Analyzer/    # ← code lives here
└── cudaTest/

## Log of Actions

### Setup birdbrain in Mike's ofice
- BirdNET was installed by Mike 
- Virtual environment (birdnet) created
- dependencies installed i think

### Test run for BirdNet on Birdbrain using CPU

# 1. Navigate to Project Folder BirdNet

 cd BirdNet

# 2. Activate virtual environment

 source birdnet/bin/activate

# 3. Navigate to BirdNET-Analyzer

 cd ~/BirdNet/BirdNET-Analyzer

# Verify installation (completed 09/22/2025)

python -m birdnet_analyzer.analyze <some-audio-file.wav>

## used

python -m birdnet_analyzer.analyze "/media/rmansfield/FatWetBird1/2025 Backyard Test Data/Data 20250204 to 20250319/SMA06024CLVW_20250318_062300.wav"

# 4. Code Settings in to Run BirdNET Analyzer 
-Set --num-threads to match the number of logical cores, which is 16.

- Tune --batch-size based on RAM availability and how well BirdNET can handle parallel workloads.
- GPT suggested: python analyze.py --num-threads 16 --batch-size 128

## Usage Guide:
birdnet_analyzer.analyze [-h] [-o OUTPUT] [--fmin FMIN] [--fmax FMAX] [--lat LAT] [--lon LON] [--week WEEK] [--sf_thresh SF_THRESH] [--slist SLIST] [--sensitivity SENSITIVITY] [--overlap OVERLAP] [--audio_speed AUDIO_SPEED] [-t THREADS] [--min_conf MIN_CONF] [-l LOCALE] [-b BATCH_SIZE] [--rtype {table,audacity,kaleidoscope,csv} [{table,audacity,kaleidoscope,csv} ...]] [--additional_columns {lat,lon,week,overlap,sensitivity,min_conf,species_list,model} [{lat,lon,week,overlap,sensitivity,min_conf,species_list,model} ...]] [--combine_results] [-c CLASSIFIER] [--skip_existing_results] [--top_n TOP_N] [--merge_consecutive MERGE_CONSECUTIVE] [--use_perch] INPUT
- more info: https://birdnet-team.github.io/BirdNET-Analyzer/usage/cli.html

## Settings currently used for annotation: 
- Min Confidence 0.1 
- Sens 1 
- Overlap 0 
- custom species list: NatesfocalbirdsplusAcousticSimilars
- output settings: Raven selection and CSV combine selection tables

python -m birdnet_analyzer.analyze \
    --min_conf 0.1 \
    --sensitivity 1 \
    --overlap 0 \
    --slist <specieslistpath> \
    --rtype csv table \
    --combine_results \
    --batch_size 128 \
    --threads 16 \
    --output <outputfilepath> \
    <inputfilepath>

- Used '/media/rmansfield/SkinnyBird1/BirdNET_GLOBAL_6K_V2.4_LabelsNatesFocalBirdsplusAcousticSimilars.txt'
- "/media/rmansfield/SkinnyBird1/2025 King Rail Project/BirdNET Output Choctaw_WMA_2025 FBplusAS" \
- "/media/rmansfield/SkinnyBird1/2025 King Rail Project/Choctaw_WMA_2025 Data"
- python -m birdnet_analyzer.analyze \
    --min_conf 0.1 \
    --sensitivity 1 \
    --overlap 0 \
    --slist "/media/rmansfield/SkinnyBird1/BirdNET_GLOBAL_6K_V2.4_LabelsNatesFocalBirdsplusAcousticSimilars.txt" \
    --rtype csv table \
    --combine_results \
    --batch_size 128 \
    --threads 16 \
    --output "/media/rmansfield/SkinnyBird1/2025 King Rail Project/BirdNET Output Choctaw_WMA_2025 FBplusAS" \
    "/media/rmansfield/SkinnyBird1/2025 King Rail Project/Choctaw_WMA_2025 Data"

started 10:53 am on 9/25/2025
finished 11:39 am
