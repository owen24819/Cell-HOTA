Cell-HOTA is an extension of HOTA. It is designed to handle cell divisions with all the benefits of HOTA. Althouhgh TrackEval has many metrics, the code was modified only to support the HOTA metric for cell tracking. All other metrics in TrackEval were not modified. This README.md was modified from the original TrackEval github.

HOTA was developed by Luiten et al. (*[HOTA: A Higher Order Metric for Evaluating Multi-Object Tracking](https://link.springer.com/article/10.1007/s11263-020-01375-2). IJCV 2020. Jonathon Luiten, Aljosa Osep, Patrick Dendorfer, Philip Torr, Andreas Geiger, Laura Leal-Taixe and Bastian Leibe.*)

Author of Cell-HOTA is Owen O'Connor and Mary Dunlop. [Link to Cell-TRACTR paper](https://www.biorxiv.org/content/10.1101/2024.07.11.603075v1)

## Running the code

The main script for running Cell-HOTA is [run_cells_challenge.py](scripts/run_cells_challenge.py).

**Example Usage:**
```python scripts/run_cells_challenge.py --MODEL CELL-TRACTR --DATASET moma --USE_FLEX_DIV True --COUNT_EDGES True```

**Required Variables:**

- `DATASET`: `str` 
   The name of the dataset you are testing (Default: `moma`).

- `MODEL`: `str` 
   The name of the mdoel whose results you are testing (Default: `Cell-TRACTR`).

- `USE_FLEX_DIV`: `bool` 
   Determines whether Cell-HOTA allows early / late divisions by one frame (Default: `True`).

- `COUNT_EDGES`: `bool` 
   Determines whether Cell-HOTA includes cells touching the edge of the image in the scoring (Default: `True`).
   
**Path Configuration:**

The `dataset` and `model` variables are used to generate the paths to the respective dataset and model directories. If needed, you can update hte default paths in the [cells_challenge.py](https://gitlab.com/dunloplab/Cell-HOTA/-/blob/master/trackeval/datasets/cells_challenge.py) script. Specifically, modifiy the `GT_FOLDER` and `TRACKERS_FOLDER` entries in the `default_config` to match your directory structure.

Ensure the data is formatted that is acceptable for the Cell Tracking Challenge or HOTA.

## Properties of this codebase

The code is written 100% in python with only numpy and scipy as minimum requirements.

The code is designed to be easily understandable and easily extendable. 

By default the code prints results to the screen, saves results out as both a summary txt file and a detailed results csv file, and outputs plots of the results. All outputs are by default saved to the 'tracker' folder for each tracker.

## Evaluate on your own custom benchmark

To evaluate on your own data, you need to format your data in the Cell Tracking Challenge format. The run_cells_challenge.py script will automatically convert the CTC formatted data into the MOTS format needed for analysis.

## Requirements
 Code tested on Python 3.7.
 
 - Minimum requirements: numpy, scipy
 - For plotting: matplotlib
 - For segmentation datasets (KITTI MOTS, MOTS-Challenge, DAVIS, YouTube-VIS): pycocotools
 - For DAVIS dataset: Pillow
 - For J & F metric: opencv_python, scikit_image
 - For simples test-cases for metrics: pytest

use ```pip3 -r install requirements.txt``` to install all possible requirements.

use ```pip3 -r install minimum_requirments.txt``` to only install the minimum if you don't need the extra functionality as listed above.

## License

Cell-HOTA is released under the [MIT License](LICENSE).
