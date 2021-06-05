from odds_data_pipe import DataLoader
from odds_plotter import Plotter

def main():
    # TODO: remove hardcoded styles here; main.py should pass this in
    styles = {
                'title' : { 'color': '#fefffe', 'weight': 'bold', 'size': 16 },
                'label' : { 'color': '#afb1b6', 'style': 'italic', 'size': 12 },
                'spline_color' : '#32323e',
                'face_color_primary' : '#252429',
                'face_color_secondary' : '#32323e',
                'grid_color' : '#53545f',
                'tick_color' : '#64636b',
                'red' : '#e5383b',
                'blue' : '#5469c4'
            }
    data = DataLoader()
    plot = Plotter(styles, data.data)
    plot._create_plots()
if __name__ == '__main__':
    main()

#####################

# from datetime import datetime
# from collections import namedtuple
# import csv
# import logging
# import matplotlib.pyplot as plt
# import numpy as np
# import os
# import pandas as pd

# # Setup constants
# DATASET_URL = 'https://www.kaggle.com/mdabbert/ufc-fights-2010-2020-with-betting-odds/download'
# GET_OUTFILE = 'data.csv'
# # Setup odds record namedtuple
# OddsRecord = namedtuple('OddsRecord',
#     [
#         'r_fighter',
#         'b_fighter',
#         'r_odds',
#         'b_odds',
#         'date',
#         'location',
#         'country',
#         'winner',
#         'title_bout',
#         'weight_class',
#         'gender'
#     ]
# )

# # Handle arguments
# parser = argparse.ArgumentParser(description= 'gather and analyze MMA odds data', epilog= 'Ready? FIGHT!')
# parser.add_argument('-v', '--verbose', help= 'add logging verbosity', action= 'store_const', dest= 'log_level', const= logging.DEBUG, default= logging.INFO)
# args = parser.parse_args()

# # Create a custom logger
# logger = logging.getLogger('mma_odds')
# logger.setLevel(logging.DEBUG)

# # Create handlers
# c_handler = logging.StreamHandler()
# f_handler = logging.FileHandler('mma_odds.log', )
# c_handler.setLevel(logging.ERROR)
# f_handler.setLevel(args.log_level) # swap between INFO and DEBUG to disable/enable debug

# # Create formatters and add it to handlers
# c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# c_handler.setFormatter(c_format)
# f_handler.setFormatter(f_format)

# # Add handlers to the logger
# logger.addHandler(c_handler)
# logger.addHandler(f_handler)

# class OddsAnalyser():
#     def __init__(self):
#         self.data = None

#     def __iter__(self):
#         """ Return iterable class."""
#         return iter(self.data)

#     def _get_data(self):
#         """ Downloads data and writes it to disk.
#             Arguments
#             ---------
#             None
#         """
#         try:
#             with open(GET_OUTFILE, 'w') as data_file:
#                 writer = csv.writer(data_file, quoting= csv.QUOTE_NONNUMERIC)
#                 resp = requests.get(DATASET_URL, stream= True)
#                 if resp.status_code != 200:
#                     logger.error(f'Response returned {resp.status_code}')
#                     resp.raise_for_status()
#                 else:
#                     logger.info(f'{DATASET_URL} returned 200 - OK')
#                     line_count = 0
#                     for line in resp.iter_lines():
#                         print(line)
#                         logging.debug(line)
#                         writer.writerow(line)
#                     logger.info(f'Wrote {line_count} lines to {GET_OUTFILE}')
#                     return True
#         except FileNotFoundError as err:
#             logger.error(f'Unexpected error writing to file {str(err)}')
#             return False

#     def _load_data(self):
#         """ Cleanses data generated from Kaggle and writes it to disk. """

#         logger.info('EXECUTING _clean_data()')

#         # Ensure we have a file to clean
#         if not os.path.exists(GET_OUTFILE):
#             logger.error(f'{GET_OUTFILE} does not exist')
#             return False
#         else:
#             try:
#                 logger.info('Reading CSV into Data Frame')
#                 # Read CSV into Data Frame
#                 df = pd.read_csv(
#                     GET_OUTFILE,
#                     sep= ',',
#                     header= 0,
#                     parse_dates= [4],
#                     infer_datetime_format= True,
#                     quotechar= '"',
#                     encoding= 'utf-8',
#                     dtype= {
#                         'R_fighter': pd.StringDtype(),
#                         'B_fighter': pd.StringDtype(),
#                         'R_odds': pd.Int16Dtype(),
#                         'B_odds': pd.Int16Dtype(),
#                         'location': pd.StringDtype(),
#                         'country': pd.StringDtype(),
#                         'Winner': pd.StringDtype(),
#                         'title_bout': pd.StringDtype(),
#                         'weight_class': pd.StringDtype(),
#                         'gender': pd.StringDtype()
#                     },
#                     skip_blank_lines= True
#                 )

#                 # Drop NA values
#                 logger.info('Dropping NaN rows')
#                 df.dropna(how= 'all', inplace= True)

#                 # Rename our columns for consistency
#                 logger.info('Renaming column headings')
#                 cols = ['r_fighter', 'b_fighter', 'r_odds', 'b_odds', 'date', 'location', 'country', 'winner', 'title_bout', 'weight_class', 'gender']
#                 df.columns = cols

#                 # Add resolved winner column with name
#                 logger.info('Resolving fight winner with fighter name')
#                 df['winner_resolved'] = [df['r_fighter'] if x.lower() == 'red' else df['b_fighter'] for x in df['winner']]

#                 # Add resolved country column with country removed from location
#                 logger.info('Resolving location name to split-out country')
#                 df['location_resolved'] = [x[0:x.rfind(',')].strip() for x in df['location']]

#                 # Clean string data
#                 logger.info('Converting string columns to lower')
#                 df['r_fighter'] = df['r_fighter'].str.lower()
#                 df['b_fighter'] = df['b_fighter'].str.lower()
#                 df['location_resolved'] = df['location_resolved'].str.lower()
#                 df['country'] = df['country'].str.lower()
#                 df['winner_resolved'] = df['winner_resolved'].str.lower()
#                 df['gender'] = df['gender'].str.lower()

#                 self.data = df

#             except Exception as err:
#                 logger.error(f'Exception occurred: {err}')

#     def _create_plots(self):
#         """ Generate plots and CSV files for analysis. """

#         logger.info('EXECUTING _create_plots()')

#         # Q1: Do the both fighters have a similar distribution of odds?

#         # Convert dataframe to numpy matrix
#         logger.info('Converting data frame to numpy array')
#         arr = self.data.to_numpy()

#         # Get all row values for r_odds and b_odds
#         x = self.data[:, 2]
#         y = self.data[:, 3]

#         # Plot histogram
#         plt.hist(
#             [x, y],
#             bins= 15,
#             color= ('#f04848', '#4878c0')
#         )

#         # Q2: How do odds vary between top weight classes?

#         # Get the weight_class array and create boolean masks for each class
#         wgt_array = self.data[:, 9]
#         lw_mask = wgt_array == 'Lightweight'
#         ww_mask = wgt_array == 'Welterweight'
#         hw_mask = wgt_array == 'Heavyweight'
#         lhw_mask = wgt_array == 'Light Heavyweight'

#         # Apply the masks to get the odds for each weight class
#         w_1 = self.data[lw_mask, 2]
#         w_2 = self.data[lw_mask, 3]
#         x_1 = self.data[ww_mask, 2]
#         x_2 = self.data[ww_mask, 3]
#         y_1 = self.data[lhw_mask, 2]
#         y_2 = self.data[lhw_mask, 3]
#         z_1 = self.data[hw_mask, 2]
#         z_2 = self.data[hw_mask, 3]

#         # Setup file output
#         weight_df = pd.DataFrame(self.data[:, [2, 3, 9]])
#         try:
#             weight_df.to_csv(
#                 path_or_buf= 'weight_data.csv',
#                 header= ['r_odds', 'b_odds', 'weight_class'],
#                 index_label= 'index',
#                 quoting= csv.QUOTE_NONNUMERIC
#             )
#         except Exception as err:
#             logger.error(err)

#         # Setup plotting
#         fig, ((axs1, axs2), (axs3, axs4), (axs5, axs6), (axs7, axs8)) = plt.subplots(4, 2)
#         fig.suptitle('Odds by Weightclass: Red vs. Blue')

#         axs1.set_title('Lightweight Red')
#         axs2.set_title('Lightweight Blue')
#         axs1.hist(w_1, bins= 25, color= '#f04848')
#         axs2.hist(w_2, bins= 25, color= '#4878c0')
#         axs3.set_title('Welterweight Red')
#         axs4.set_title('Welterweight Blue')
#         axs3.hist(x_1, bins= 25, color= '#f04848')
#         axs4.hist(x_2, bins= 25, color= '#4878c0')
#         axs5.set_title('Light Heavyweight Red')
#         axs6.set_title('Light Heavyweight Blue')
#         axs5.hist(y_1, bins= 25, color= '#f04848')
#         axs6.hist(y_2, bins= 25, color= '#4878c0')
#         axs7.set_title('Heavyweight Red')
#         axs8.set_title('Heavyweight Blue')
#         axs7.hist(z_1, bins= 25, color= '#f04848')
#         axs8.hist(z_2, bins= 25, color= '#4878c0')

#         # Q3: How do the odds vary by gender?

#         # Get the gender array and create boolean masks for each gender
#         gender_array = self.data[:, 10]
#         m_mask = gender_array == 'MALE'
#         f_mask = gender_array == 'FEMALE'

#         # Apply the masks to get the odds for each gender
#         a_1 = self.data[f_mask, 2]
#         a_2 = self.data[f_mask, 3]
#         b_1 = self.data[m_mask, 2]
#         b_2 = self.data[m_mask, 3]

#         # Setup file output
#         gender_df = pd.DataFrame(self.data[:, [2, 3, 10]])
#         try:
#             gender_df.to_csv(
#                 path_or_buf= 'gender_data.csv',
#                 header= ['r_odds', 'b_odds', 'gender'],
#                 index_label= 'index',
#                 quoting= csv.QUOTE_NONNUMERIC
#             )
#         except Exception as err:
#             logger.error(err)

#         # Setup plotting
#         fig, ((axs1, axs2), (axs3, axs4)) = plt.subplots(2, 2)
#         fig.suptitle('Odds by Gender: Red vs. Blue')

#         axs1.set_title('Female Red')
#         axs2.set_title('Female Blue')
#         axs1.hist(a_1, bins= 25, color= '#f04848')
#         axs2.hist(a_2, bins= 25, color= '#4878c0')
#         axs3.set_title('Male Red')
#         axs4.set_title('Male Blue')
#         axs3.hist(b_1, bins= 25, color= '#f04848')
#         axs4.hist(b_2, bins= 25, color= '#4878c0')

#         # Plot
#         plt.tight_layout()
#         plt.show()
