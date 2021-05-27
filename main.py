import argparse
from datetime import datetime
from collections import namedtuple
import csv
import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Import custom modules
from mma_odds import OddsAnalyser

# Handle arguments
parser = argparse.ArgumentParser(description= 'run an analysis of MMA fighter and odds data', epilog= 'Ready? FIGHT!')
parser.add_argument('-v', '--verbose', help= 'add logging verbosity', action= 'store_const', dest= 'log_level', const= logging.DEBUG, default= logging.INFO)
parser.add_argument('-pi', '--plot-initial')
parser.add_argument('-pf', '--plot-final')
parser.add_argument('-o', '--output')
# parser.add_argument() # TODO: Add additional argument
args = parser.parse_args()

# Create a custom logger
logger = logging.getLogger('mma_odds')
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('mma_odds.log', )
c_handler.setLevel(logging.ERROR)
f_handler.setLevel(args.log_level) # swap between INFO and DEBUG to disable/enable debug

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

class DataMashup():
    def __init__(self):
        self.odds_data = None
        self.fighter_data = None
        self.aggregate_data = None

    def _import_odds_data(self, dataset):
        """ Imports odds data. """
        if not isinstance(dataset, np.ndarray):
            logger.error('Odds dataset required!')
            raise Exception('Odds dataset required!')
        else:
            self.odds_data = dataset

    def _combine_data(self, odds_dataset, fight_dataset):
        """ Combines two datasets into a single numpy array. 
        
            Arguments
            ---------
            odds_dataset: ndarray; REQUIRED
                The entire odds dataset as a numpy array.
            fight_dataset: ndarray; REQUIRED
                The entire fight dataset as a numpy array.
        """
        logger.info('EXECUTING _combine_data()')
        # Verify datasets before combining
        if not isinstance(odds_dataset, np.ndarray) or not isinstance(fight_dataset, np.ndarray):
            logger.error('Two numpy arrays required!')
            raise Exception('Two numpy arrays required!')
        else:
            self.aggregate_data = np.concatenate(odds_dataset, fight_dataset)

    def _method_2(self):
        pass

def main():
    # Get odds data, load it, and generate the necessary plots
    odds = OddsAnalyser()
    odds._load_data()
    odds._create_plots()

    # Load odds data and fight data
    analyser = DataMashup()
    analyser._import_odds_data(odds.data)
    print(analyser.odds_data[0])

if __name__ == '__main__':
    main()