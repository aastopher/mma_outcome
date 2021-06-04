import argparse
import logging
from collections import namedtuple
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Import custom modules
from mma_odds import OddsAnalyser

# Handle arguments
parser = argparse.ArgumentParser(description= 'run an analysis of MMA fighter and odds data', epilog= 'Ready? FIGHT!')
parser.add_argument('-v', '--verbose', help= 'add logging verbosity', action= 'store_const', dest= 'log_level', const= logging.DEBUG, default= logging.INFO)
parser.add_argument('-d', '--dark-mode', help= 'add dark mode to plotting', action= 'store_true', dest= 'dark_mode')
# parser.add_argument('-e', '--explore', help= 'explore initial dataset plots', action= 'store_true', dest= 'explore')
# parser.add_argument('-a', '--analyze', help= 'explore final analysis plots', action= 'store_true', dest= 'analyze')
# parser.add_argument('-o', '--output', help= 'define a prefix for all export data', action= 'store_const', const= 'output_prefix')
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

    def _import_odds_data(self, dataset, which_dataset):
        """ Imports odds or fighter data into the class. """
        if not isinstance(dataset, pd.DataFrame):
            logger.error('Dataframe required!')
            raise Exception('Dataframe required!')
        else:
            # Import the appropriate dataset to the attribute
            if which_dataset == 'odds':
                self.odds_data = dataset
                logger.info('Odds data loaded')
            elif which_dataset == 'fighter':
                self.fighter_data = dataset
                logger.info('Fighter data loaded')

    def _merge_data(self):
        """ Combines two datasets into a single numpy array. """
        logger.info('EXECUTING _merge_data()')
        # Attempt merge on fighter data keys
        try:
            master = self.odds_data.merge(self.fighter_data, on= ['r_fighter', 'b_fighter'])
            master.set_index([0], 'index')
            logger.info('Merged data on r_fighter and b_fighter keys')
        except Exception as err:
            logger.error(f'Error merging dataframes: {err}')

        # Load data into class attribute and write combined data to file
        self.aggregate_data = master
        master.to_csv('merged_master_data.csv', sep= ',')
        logger.info('Exported master data to CSV')

    def _scatter_odds_vs_reach(self, plot, dark_mode= False):
        """ Plots a scatter plot of fighter reach vs the vegas odds.

        Args:
            plot (Boolean): Indicates whether to plot the output or not.
            dark_mode (Boolean): Indicates whether plot in dark color scheme.
        """

        # Subset data for odds and reach
        odds_reach = self.aggregate_data[['r_odds', 'r_reach', 'b_odds', 'b_reach']]

        # Convert to numpy array
        # arr = odds_reach.to_numpy()

        # Fill empty rows to avoid annoying Pandas errors
        odds_reach.loc[:, 'reach_high'] = np.nan
        odds_reach.loc[:, 'reach_low'] = np.nan
        odds_reach.loc[:, 'odds_reach_high'] = np.nan
        odds_reach.loc[:, 'odds_reach_low'] = np.nan
        odds_reach.loc[:, 'reach_advantage'] = ''

        # Mutate dataframe to indicate reach advantage and associated odds
        for index, row in odds_reach.iterrows():
            if row['r_reach'] > row['b_reach']:
                # Add column with r fighter reach and indicate reach advantage
                odds_reach.loc[index, 'reach_high'] = row['r_reach']
                odds_reach.loc[index, 'reach_high'] = row['r_reach']
                odds_reach.loc[index, 'odds_reach_high'] = row['r_odds']
                odds_reach.loc[index, 'odds_reach_low'] = row['b_odds']
                odds_reach.loc[index, 'reach_low'] = row['b_reach']
                odds_reach.loc[index, 'reach_advantage'] = 'r_fighter'
            elif row['r_reach'] < row['b_reach']:
                # Add column with rbfighter reach and indicate reach advantage
                odds_reach.loc[index, 'reach_high'] = row['b_reach']
                odds_reach.loc[index, 'reach_low'] = row['r_reach']
                odds_reach.loc[index, 'odds_reach_high'] = row['b_odds']
                odds_reach.loc[index, 'odds_reach_low'] = row['r_odds']
                odds_reach.loc[index, 'reach_advantage'] = 'b_fighter'

        # Filter out rows in which the fighter reaches were the same
        filtered_odds_reach = odds_reach[odds_reach.reach_advantage != '']
        advantage_odds_reach = filtered_odds_reach[['reach_high', 'odds_reach_high']]
        disadvantage_odds_reach = filtered_odds_reach[['reach_low', 'odds_reach_low']]
        # Calculate averages for advantage and no-advantage
        high = advantage_odds_reach.groupby('reach_high').mean('odds_reach_high')
        low = disadvantage_odds_reach.groupby('reach_low').mean('odds_reach_low')
        # Calculate the regression lines
        hm, hb = np.polyfit(high.index, high[['odds_reach_high']], 1)
        lm, lb = np.polyfit(low.index, low[['odds_reach_low']], 1)

        # Output dataset to CSV
        odds_reach.to_csv(args.output_file + 'raw.csv', sep= ',')
        filtered_odds_reach.to_csv(args.output_file + '_grouped.csv', sep= ',')

        # Plot scatters
        if plot:
            # Setup basic plotting structure
            fig_1, ax_1 = plt.subplots(nrows= 2, ncols= 1)
            fig_1.set_size_inches(13, 10)
            fig_2, ax_2 = plt.subplots()
            fig_2.set_size_inches(13, 10)

            if dark_mode:
                # Setup dark font dictionary
                title = { 'color': '#fefffe', 'weight': 'bold', 'size': 16 }
                label = { 'color': '#afb1b6', 'style': 'italic', 'size': 12 }
                spline_color = '#32323e'
                face_color_primary = '#252429'
                face_color_secondary = '#32323e'
                grid_color = '#53545f'
                tick_color = '#64636b'
                red = '#e5383b'
                blue = '#5469c4'
            else:
                # Setup light font dictionary
                title = { 'color': '#2c2d2c', 'weight': 'bold', 'size': 16 }
                label = { 'color': '#989a98', 'style': 'italic', 'size': 12 }
                spline_color = '#32323e'
                face_color_primary = '#f5f6f5'
                face_color_secondary = '#fefffe'
                grid_color = '#53545f'
                tick_color = '#64636b'
                red = '#e5383b'
                blue = '#5469c4'
            
            # Setup titles and labels with styles
            ax_1[0].set_title('Relationship Between Vegas Odds and (Red) Fighter Reach vs. (Blue) Fighter Reach', fontdict= title)
            ax_1[0].set_xlabel('Fighter Reach (Inches)', fontdict= label)
            ax_1[0].set_ylabel('Vegas Odds', fontdict= label)
            ax_1[1].set_xlabel('Fighter Reach (Inches)', fontdict= label)
            ax_1[1].set_ylabel('Vegas Odds', fontdict= label)

            # Setup colors for first plot
            fig_1.patch.set_facecolor(face_color_primary)
            ax_1[0].grid(color= grid_color, linestyle= '--', linewidth=0.7)
            ax_1[0].spines['bottom'].set_color(spline_color)
            ax_1[0].spines['top'].set_color(spline_color)
            ax_1[0].spines['left'].set_color(spline_color)
            ax_1[0].spines['right'].set_color(spline_color)
            ax_1[1].grid(color= grid_color, linestyle= '--', linewidth=0.7)
            ax_1[1].spines['bottom'].set_color(spline_color)
            ax_1[1].spines['top'].set_color(spline_color)
            ax_1[1].spines['left'].set_color(spline_color)
            ax_1[1].spines['right'].set_color(spline_color)
            # Set the ticks
            ax_1[0].tick_params(colors= tick_color)
            ax_1[1].tick_params(colors= tick_color)
            # Set the subplot facecolor
            ax_1[0].patch.set_facecolor(face_color_secondary)
            ax_1[1].patch.set_facecolor(face_color_secondary)

            ax_2.set_title('Relationship Between (Average) Vegas Odds and Fighter Reach', fontdict= title)
            ax_2.set_xlabel('Vegas Odds', fontdict= label)
            ax_2.set_ylabel('Fighter Reach (Inches)', fontdict= label)

            # Setup colors for second plot
            fig_2.patch.set_facecolor(face_color_primary)
            ax_2.grid(color= grid_color, linestyle= '--', linewidth=0.7)
            ax_2.spines['bottom'].set_color(spline_color)
            ax_2.spines['top'].set_color(spline_color)
            ax_2.spines['left'].set_color(spline_color)
            ax_2.spines['right'].set_color(spline_color)
            ax_2.grid(color= grid_color, linestyle= '--', linewidth=0.7)
            ax_2.spines['bottom'].set_color(spline_color)
            ax_2.spines['top'].set_color(spline_color)
            ax_2.spines['left'].set_color(spline_color)
            ax_2.spines['right'].set_color(spline_color)
            # Set the ticks
            ax_2.tick_params(colors= tick_color)
            ax_2.tick_params(colors= tick_color)
            # Set the subplot facecolor
            ax_2.patch.set_facecolor(face_color_secondary)
            ax_2.patch.set_facecolor(face_color_secondary)

            # Plot avg. odds vs. reach using index since groupby adds the grouping column as index
            ax_1[0].scatter(x= filtered_odds_reach[['r_reach']], y= filtered_odds_reach[['r_odds']], color= red, alpha= 0.4, label= 'Red Fighter Reach')
            ax_1[1].scatter(x= filtered_odds_reach[['b_reach']], y= filtered_odds_reach[['b_odds']], color= blue, alpha= 0.4, label= 'Blue Fighter Reach')

            # Plot avg. odds vs. reach using index since groupby adds the grouping column as index
            ax_2.scatter(x= high.index, y= high[['odds_reach_high']], color= red, s= 40, label= 'Reach Advantage')
            ax_2.scatter(x= low.index, y= low[['odds_reach_low']], color= blue, label= 'Reach Disadvantage')
            ax_2.legend()
            ax_2.plot(high.index, hm * high.index + hb, color= red, linestyle= '--')
            ax_2.plot(low.index, lm * low.index + lb, color= blue, linestyle= '--')

            plt.show()

def main():
    # Get odds data, load it, and generate the necessary plots
    odds = OddsAnalyser()
    odds._load_data()
    # odds._create_plots() 

    # Load odds data and fight data
    analyser = DataMashup()
    analyser._import_odds_data(odds.data, 'odds')

    # TODO: replace with true code
    # loads processed data into DataMashup()
    df = pd.read_csv(
        'processed_data.csv',
        sep= ',',
        header= 0,
        quotechar= '"',
        encoding= 'utf-8',
        dtype= {
            'r_fighter': pd.StringDtype(),
            'r_reach': pd.Int16Dtype(),
            'b_fighter': pd.StringDtype(),
            'b_reach': pd.Int16Dtype(),
            'winner': pd.StringDtype(),
            'reach_win': pd.BooleanDtype()
        },
        skip_blank_lines= True
    )
    df['r_fighter'] = df['r_fighter'].str.lower()
    df['b_fighter'] = df['b_fighter'].str.lower()
    df['winner'] = df['winner'].str.lower()
    analyser.fighter_data = df

    # Combine dataframes
    analyser._merge_data()

    # Analysis: Do the Vegas odds follow the fighter with better reach?
    analyser._scatter_odds_vs_reach(True, False)

    # if args.dark_mode:
    #     analyser._scatter_odds_vs_reach(True, True)
    # else:
    #     analyser._scatter_odds_vs_reach(True, False)

if __name__ == '__main__':
    main()