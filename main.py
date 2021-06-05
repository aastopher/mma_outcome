import argparse
import logging
from collections import namedtuple
import csv, os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Import custom modules
from modules.odds_data_pipe import DataLoader
from modules.fighter_data_pipe import CalculatedData
from modules.odds_plotter import Plotter as OddsPlotter
from modules.fighter_plotter import Plotter as FighterPlotter
from modules.cli_logger import CLILogger

# Define styling
DARK_STYLE = {
    'title' : { 'color': '#fefffe', 'weight': 'bold', 'size': 16 },
    'label' : { 'color': '#afb1b6', 'style': 'italic', 'size': 12 },
    'spline_color' : '#32323e',
    'face_color_primary' : '#252429',
    'face_color_secondary' : '#32323e',
    'grid_color' : '#53545f',
    'tick_color' : '#64636b',
    'red' : '#e5383b',
    'blue' : '#5469c4'}
LIGHT_STYLE = {
    'title' : { 'color': '#2c2d2c', 'weight': 'bold', 'size': 16 },
    'label' : { 'color': '#989a98', 'style': 'italic', 'size': 12 },
    'spline_color' : '#32323e',
    'face_color_primary' : '#f5f6f5',
    'face_color_secondary' : '#fefffe',
    'grid_color' : '#53545f',
    'tick_color' : '#64636b',
    'red' : '#e5383b',
    'blue' : '#5469c4'}

#instantiate main logger and cli
cli = CLILogger('analyser',['DataMashup'])
logger = logging.getLogger('DataMashup')

# Set prefix correctly if empty
if cli.args.command == None or cli.args.output[0] == '':
    prefix = ''
else:
    prefix = cli.args.output[0] + '_'

class DataMashup():
    def __init__(self):
        self.odds_data = None
        self.fighter_data = None
        self.aggregate_data = None

    def _import_data(self, dataset, which_dataset):
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
            logger.info('Merged data on r_fighter and b_fighter keys')
        except Exception as err:
            logger.error(f'Error merging dataframes: {err}')

        # Load data into class attribute and write combined data to file
        self.aggregate_data = master
        master.to_csv('data_output/merged_master_data.csv', sep= ',')
        logger.info('Exported master data to CSV')

    def _scatter_odds_vs_reach(self, style, plot):
        """ Plots a scatter plot of fighter reach vs the vegas odds.

        Args:
            plot (Boolean): Indicates whether to plot the output or not.
            style (Dict): Dictionary of styling.
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
        #TODO: Fix this
        # odds_reach.to_csv(args.output_file + 'raw.csv', sep= ',')
        # filtered_odds_reach.to_csv(args.output_file + '_grouped.csv', sep= ',')

        # Plot scatters
        if plot:
            # Setup basic plotting structure
            fig_1, ax_1 = plt.subplots(nrows= 2, ncols= 1)
            fig_1.set_size_inches(13, 10)
            fig_2, ax_2 = plt.subplots()
            fig_2.set_size_inches(13, 10)

            # Setup titles and labels with styles
            ax_1[0].set_title('Relationship Between Vegas Odds and (Red) Fighter Reach vs. (Blue) Fighter Reach', fontdict= style['title'])
            ax_1[0].set_xlabel('Fighter Reach (Inches)', fontdict= style['label'])
            ax_1[0].set_ylabel('Vegas Odds', fontdict= style['label'])
            ax_1[1].set_xlabel('Fighter Reach (Inches)', fontdict= style['label'])
            ax_1[1].set_ylabel('Vegas Odds', fontdict= style['label'])

            # Setup colors for first plot
            fig_1.patch.set_facecolor(style['face_color_primary'])
            ax_1[0].grid(color= style['grid_color'], linestyle= '--', linewidth=0.7)
            ax_1[0].spines['bottom'].set_color(style['spline_color'])
            ax_1[0].spines['top'].set_color(style['spline_color'])
            ax_1[0].spines['left'].set_color(style['spline_color'])
            ax_1[0].spines['right'].set_color(style['spline_color'])
            ax_1[1].grid(color= style['grid_color'], linestyle= '--', linewidth=0.7)
            ax_1[1].spines['bottom'].set_color(style['spline_color'])
            ax_1[1].spines['top'].set_color(style['spline_color'])
            ax_1[1].spines['left'].set_color(style['spline_color'])
            ax_1[1].spines['right'].set_color(style['spline_color'])
            # Set the ticks
            ax_1[0].tick_params(colors= style['tick_color'])
            ax_1[1].tick_params(colors= style['tick_color'])
            # Set the subplot facecolor
            ax_1[0].patch.set_facecolor(style['face_color_secondary'])
            ax_1[1].patch.set_facecolor(style['face_color_secondary'])

            ax_2.set_title('Relationship Between (Average) Vegas Odds and Fighter Reach', fontdict= style['title'])
            ax_2.set_xlabel('Vegas Odds', fontdict= style['label'])
            ax_2.set_ylabel('Fighter Reach (Inches)', fontdict= style['label'])

            # Setup colors for second plot
            fig_2.patch.set_facecolor(style['face_color_primary'])
            ax_2.grid(color= style['grid_color'], linestyle= '--', linewidth=0.7)
            ax_2.spines['bottom'].set_color(style['spline_color'])
            ax_2.spines['top'].set_color(style['spline_color'])
            ax_2.spines['left'].set_color(style['spline_color'])
            ax_2.spines['right'].set_color(style['spline_color'])
            ax_2.grid(color= style['grid_color'], linestyle= '--', linewidth=0.7)
            ax_2.spines['bottom'].set_color(style['spline_color'])
            ax_2.spines['top'].set_color(style['spline_color'])
            ax_2.spines['left'].set_color(style['spline_color'])
            ax_2.spines['right'].set_color(style['spline_color'])
            # Set the ticks
            ax_2.tick_params(colors= style['tick_color'])
            ax_2.tick_params(colors= style['tick_color'])
            # Set the subplot facecolor
            ax_2.patch.set_facecolor(style['face_color_secondary'])
            ax_2.patch.set_facecolor(style['face_color_secondary'])

            # Plot avg. odds vs. reach using index since groupby adds the grouping column as index
            ax_1[0].scatter(x= filtered_odds_reach[['r_reach']], y= filtered_odds_reach[['r_odds']], color= style['red'], alpha= 0.4, label= 'Red Fighter Reach')
            ax_1[1].scatter(x= filtered_odds_reach[['b_reach']], y= filtered_odds_reach[['b_odds']], color= style['blue'], alpha= 0.4, label= 'Blue Fighter Reach')

            # Plot avg. odds vs. reach using index since groupby adds the grouping column as index
            ax_2.scatter(x= high.index, y= high[['odds_reach_high']], color= style['red'], s= 40, label= 'Reach Advantage')
            ax_2.scatter(x= low.index, y= low[['odds_reach_low']], color= style['blue'], label= 'Reach Disadvantage')
            ax_2.legend()
            ax_2.plot(high.index, hm * high.index + hb, color= style['red'], linestyle= '--')
            ax_2.plot(low.index, lm * low.index + lb, color= style['blue'], linestyle= '--')

            plt.savefig(f'data_output/{prefix}odds_reach')
            # plt.show()

def main():
    def _load_data_sets():
        # Get both datasets
        odds_data = DataLoader()
        fighter_data = CalculatedData()
        return odds_data,fighter_data

    def _load_analyser():
        odds_data,fighter_data = _load_data_sets()
        # Load odds data and fight data
        analyser = DataMashup()
        analyser._import_data(odds_data.data, 'odds')
        analyser._import_data(fighter_data.data, 'fighter')

        # Combine dataframes
        analyser._merge_data()

        return odds_data,fighter_data,analyser

    # Handle 'explore' command
    if cli.args.command == 'explore':
        odds_data,fighter_data = _load_data_sets()
        if cli.args.dark_mode:
            odds_plotter = OddsPlotter(DARK_STYLE, odds_data.data)
            fighter_plotter = FighterPlotter(DARK_STYLE, fighter_data.data)
        else:
            odds_plotter = OddsPlotter(LIGHT_STYLE, odds_data.data)
            fighter_plotter = FighterPlotter(LIGHT_STYLE, fighter_data.data)
        odds_plotter._create_plots()
        fighter_plotter._create_plots()

    # Handle 'analyze' command
    if cli.args.command == 'analyze':
        odds_data,fighter_data,analyser = _load_analyser()
        if cli.args.dark_mode:
            analyser._scatter_odds_vs_reach(DARK_STYLE, True)
        else:
            analyser._scatter_odds_vs_reach(LIGHT_STYLE, True)

    # Handle 'deep' command
    if cli.args.command == 'deep':
        odds_data,fighter_data,analyser = _load_analyser()
        if cli.args.dark_mode:
            odds_plotter = OddsPlotter(DARK_STYLE, odds_data.data)
            fighter_plotter = FighterPlotter(DARK_STYLE, fighter_data.data)
            analyser._scatter_odds_vs_reach(DARK_STYLE, True)
        else:
            odds_plotter = OddsPlotter(LIGHT_STYLE, odds_data.data)
            fighter_plotter = FighterPlotter(LIGHT_STYLE, fighter_data.data)
            analyser._scatter_odds_vs_reach(LIGHT_STYLE, True)
        odds_plotter._create_plots()
        fighter_plotter._create_plots()

if __name__ == '__main__':
    main()
