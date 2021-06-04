### MODULE: responsible for all plotting functions ###

import logging, csv, os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
sys.path.append("mma_reach_height/modules/")
from cli_logger import *

#instantiate cli args and class loggers using cli_logger module
CLILogger('plotter',['Plotter'])
plotterLogger = logging.getLogger('Plotter')

class Plotter:
    def __init__(self,data=None):
        plotterLogger.debug(f'Plotter instantiated')
        self.data = data
        self._win_plot('reach')
        self._win_plot('height')
        self._win_type_plot('reach')
        self._win_type_plot('height')
    def _win_plot(self, reach_height):
        plotterLogger.info(f'plotting {reach_height} wins')
        if reach_height == 'reach':
            wins = self.data['reach_win'].tolist().count(True)
            losses = self.data['reach_win'].tolist().count(False)
            labels = ['long reach wins', 'short reach wins']
        if reach_height == 'height':
            labels = ['tall wins', 'short wins']
            wins = self.data['height_win'].tolist().count(True)
            losses = self.data['height_win'].tolist().count(False)
        data = [float(wins/len(self.data))*100,float(losses/len(self.data))*100]

        fig, ax = plt.subplots(figsize =(10, 7))
        wedges, texts, autotexts = ax.pie(data,
                                          autopct = '%.1f%%',
                                          labels = labels,
                                          colors = ('#4F82BC','#C0504E'),
                                          startangle = 90,
                                          textprops = dict(color ="black"))

        ax.legend(wedges, labels,
                  title =f"{reach_height} wins-losses",
                  loc ="upper left",
                  bbox_to_anchor =(1, 0, 0.5, 1))

        plt.setp(autotexts, size = 8, weight ="bold")
        ax.set_title(f"{reach_height} win-loss distribution")

        plt.savefig(f'mma_reach_height/data_output/{reach_height}_pie')
    #NOT WORKING
    def _win_type_plot(self, reach_height):
        plotterLogger.info(f'plotting {reach_height} win types')
        if reach_height == 'reach':
            print('reach')
            wins = self.data[f'{reach_height}_win'].tolist()
        if reach_height == 'height':
            wins = self.data[f'{reach_height}_win'].tolist()
        win_types = set(self.data['win_type'].tolist())
        print(wins)
        wins = self.data[f'{reach_height}_win'].tolist().count(True)
        plt.style.use('fast')
        plt.figure(figsize=(10,10))
        x_pos = [i*2 for i, _ in enumerate(win_types)]
        plt.bar(x_pos, wins, width=1)
        plt.xlabel('Win Types')
        plt.ylabel(f'{reach_height} Wins')
        plt.title(f"{reach_height} Wins Per Win Type")
        plt.xticks(x_pos, win_types, rotation=45)
        plt.tight_layout()
        plt.savefig(f'mma_reach_height/data_output/{reach_height}_wins_per_win_type')

        data = set(self.data['win_type'].tolist())
        # print(data)
