## How To: Diana's Code
I have 2 scripts which I believe you will need to get the training data setup and ready for running few-shots.

### convert_annotations.ipynb
This is where you would generate a single csv file called `combined_annotations.csv` for both the standard and background samples. This is used to get all of the valid clips (those that have been 2-person checked). Run this script over the folder where all your annotation csvs are!
* Be sure to have the column headers in the original csvs be consistent.. these are used later to pull out important info in the csvs. For example, please make sure these are included in the csvs and match exactly:
    
    * `"Begin Path"`
    * `"File Offset (s)"`
    * `"Common Name"`

To run this notebook file, you press the 'play' button to the left of both cells (a cell is a chunk of code within a Python Notebook). Be sure to run the cells in order.

### generate_multihot.py
This takes the generated `combined_annotations.csv` and creates new 3 seconds .wav files which are multi-hot labeled, as well as `annotations_multilabel.csv`. All you need to do with this is make sure that the file paths are correct. The only other thing that could happen is that you changed the column headers in the original annotation csvs (I mentioned this in the 'convert_annotations.ipynb' section).

The following are the variables that might need updated paths:

* `LABEL_CSV_PATH` : The path to `combined_annotations.csv` which is generated from the convert_annotations.ipynb script
* `BG_CSV_PATH` : The path to `combined_annotations.csv` for background clips which is generated from the convert_annotations.ipynb script
* `OUTPUT_AUDIO_DIR` : The 3 second clips will be saved to the path specified here
* `BACKGROUND_DIR` : The 3 second background clips will be saved to the path specified here
* `OUTPUT_CSV_PATH` : The annotations csv where the multilabel information goes, this is the    `training_data_annotations.csv` which is used for training

