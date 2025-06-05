""" run_cells_challenge.py

Run example:
run_cells_challenge.py --GT_FOLDER /path/to/gt --TRACKERS_FOLDER /path/to/trackers --USE_PARALLEL False --METRICS Hota

Command Line Arguments: Defaults, # Comments
    Required arguments:
        'GT_FOLDER': None,  # Location of GT data
        'TRACKERS_FOLDER': None,  # Location of tracker results
    Eval arguments:
        'USE_PARALLEL': False,
        'NUM_PARALLEL_CORES': 8,
        'BREAK_ON_ERROR': True,
        'PRINT_RESULTS': True,
        'PRINT_ONLY_COMBINED': False,
        'PRINT_CONFIG': True,
        'TIME_PROGRESS': True,
        'OUTPUT_SUMMARY': True,
        'OUTPUT_DETAILED': True,
        'PLOT_CURVES': True,
    Dataset arguments:
        'OUTPUT_FOLDER': None,  # Where to save eval results (if None, same as TRACKERS_FOLDER)
        'TRACKERS_TO_EVAL': None,  # Filenames of trackers to eval (if None, all in folder)
        'CLASSES_TO_EVAL': ['cell'],  # Valid: ['cell']
        'SPLIT_TO_EVAL': 'test',  # Valid: 'train', 'test'
        'INPUT_AS_ZIP': False,  # Whether tracker input files are zipped
        'PRINT_CONFIG': True,  # Whether to print current config
        'TRACKER_SUB_FOLDER': 'data',  # Tracker files are in TRACKER_FOLDER/tracker_name/TRACKER_SUB_FOLDER
        'OUTPUT_SUB_FOLDER': '',  # Output files are saved in OUTPUT_FOLDER/tracker_name/OUTPUT_SUB_FOLDER
        'SEQMAP_FOLDER': None,  # Where seqmaps are found (if None, GT_FOLDER/seqmaps)
        'SEQMAP_FILE': None,  # Directly specify seqmap file (if none use seqmap_folder/cells-split_to_eval)
        'SEQ_INFO': None,  # If not None, directly specify sequences to eval and their number of timesteps
        'GT_LOC_FORMAT': '{gt_folder}/{seq}/gt/gt.txt',  # '{gt_folder}/{seq}/gt/gt.txt'
        'SKIP_SPLIT_FOL': False,    # If False, data is in GT_FOLDER/cells-SPLIT_TO_EVAL/ and in
                                    # TRACKERS_FOLDER/cells-SPLIT_TO_EVAL/tracker/
                                    # If True, then the middle 'cells-split' folder is skipped for both.
    Metric arguments:
        'METRICS': ['HOTA','CLEAR', 'Identity', 'VACE', 'JAndF']
"""

import sys
import os
import argparse
from pathlib import Path
from multiprocessing import freeze_support

code_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, code_path)

import trackeval  # noqa: E402
import time
from trackeval.utils import convert_CTC_to_MOTS

if __name__ == '__main__':
    freeze_support()

    # Command line interface:
    default_eval_config = trackeval.Evaluator.get_default_eval_config()
    default_eval_config['DISPLAY_LESS_PROGRESS'] = False
    default_dataset_config = trackeval.datasets.CellsChallenge.get_default_dataset_config()
    default_metrics_config = {'METRICS': ['HOTA', 'CLEAR', 'Identity']}
    config = {**default_eval_config, **default_dataset_config, **default_metrics_config}  # Merge default configs
    
    parser = argparse.ArgumentParser()
    # Add required arguments first
    parser.add_argument('--GT_FOLDER', required=True, help='Path to ground truth data')
    parser.add_argument('--TRACKERS_FOLDER', required=True, help='Path to tracker results')
    
    # Add optional arguments
    for setting in config.keys():
        if setting not in ['GT_FOLDER', 'TRACKERS_FOLDER']:  # Skip already added required args
            if type(config[setting]) == list or type(config[setting]) == type(None):
                parser.add_argument("--" + setting, nargs='+')
            else:
                parser.add_argument("--" + setting)
    
    args = parser.parse_args().__dict__
    for setting in args.keys():
        if args[setting] is not None:
            if type(config[setting]) == type(True):
                if args[setting] == 'True':
                    x = True
                elif args[setting] == 'False':
                    x = False
                else:
                    raise Exception('Command line parameter ' + setting + 'must be True or False')
            elif type(config[setting]) == type(1):
                x = int(args[setting])
            elif type(args[setting]) == type(None):
                x = None
            elif setting == 'SEQ_INFO':
                x = dict(zip(args[setting], [None]*len(args[setting])))
            else:
                x = args[setting]
            config[setting] = x
    
    eval_config = {k: v for k, v in config.items() if k in default_eval_config.keys()}
    dataset_config = {k: v for k, v in config.items() if k in default_dataset_config.keys()}
    metrics_config = {k: v for k, v in config.items() if k in default_metrics_config.keys()}

    # Convert results to HOTA format if necessary
    tracker_path = Path(config['TRACKERS_FOLDER'])
    # Remove CTC from end of path if present, add HOTA if not present
    parts = tracker_path.parts
    if parts[-1] == 'CTC':
        tracker_path = Path(*parts[:-1])
    if parts[-1] != 'HOTA':
        tracker_path = tracker_path / 'HOTA'
    config['TRACKERS_FOLDER'] = str(tracker_path)
    if not tracker_path.exists():
        ctc_path = tracker_path.parent / 'CTC'
        if not ctc_path.exists():
            raise Exception(f'Neither HOTA format path ({tracker_path}) nor CTC format path ({ctc_path}) exists')
        convert_CTC_to_MOTS(hotapath=tracker_path, ctcpath=ctc_path)

    # Convert ground truths to HOTA format if necessary
    gt_path = Path(config['GT_FOLDER'])
    gt_path = gt_path.parent / 'test-HOTA'
    if not gt_path.exists():
        ctc_path = gt_path.parents[1] / 'CTC' / 'test'
        if not ctc_path.exists():
            raise Exception(f'Neither HOTA format path ({gt_path}) nor CTC format path ({ctc_path}) exists')
        convert_CTC_to_MOTS(hotapath=gt_path, ctcpath=ctc_path)

    start_time = time.time()
    # Run code
    evaluator = trackeval.Evaluator(eval_config)
    dataset_list = [trackeval.datasets.CellsChallenge(dataset_config)]
    metrics_list = []
    for metric in [trackeval.metrics.HOTA]:
        if metric.get_name() in metrics_config['METRICS']:
            metrics_list.append(metric(config['USE_FLEX_DIV']))
    if len(metrics_list) == 0:
        raise Exception('No metrics selected for evaluation')
    evaluator.evaluate(dataset_list, metrics_list)

    end_time = time.time()
    diff = end_time - start_time
    print(f'It took {round(diff,3)} seconds')