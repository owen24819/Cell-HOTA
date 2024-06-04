Cell-HOTA is an extention of HOTA. It is designed to handle cell divisions with all the benefits of HOTA. Althouhgh TrackEval has many metrics, the code was modified only to support the HOTA metric for cell tracking. All other metrics in TrackEval were not modified. This README.md was modified from the original TrackEval github.

HOTA was developed by Luiten et al. (*[HOTA: A Higher Order Metric for Evaluating Multi-Object Tracking](https://link.springer.com/article/10.1007/s11263-020-01375-2). IJCV 2020. Jonathon Luiten, Aljosa Osep, Patrick Dendorfer, Philip Torr, Andreas Geiger, Laura Leal-Taixe and Bastian Leibe.*)

Author of Cell-HOTA is Owen O'Connor and Mary Dunlop (link to paper)

## Running the code

[here](scripts/run_cells_challenge.py) is the main script called run_cells_challenge.py. 

You need to set 4 variables to run it properly:

dataset: str - the name of the dateset you are testing
 
model: str - the name of the model whose results you are testing
   
gt_path: Pathlib path - the path to the ground truth

res_path: Pathlib path - the path to the model results

There are 2 optional varialbes:

flex_div: bool (default: True) - determines whether Cell-HOTA allows flexible divisions
   
count_edges: bool (default: True) - determines whether Cell-HOTA uses cells touching the edge of the images towards the score

See each script for instructions and arguments. Ensure the data is formatted in the Cell Tracking Challege format.

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
