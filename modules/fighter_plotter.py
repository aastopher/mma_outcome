### MODULE: responsible for all plotting functions ###

import logging, csv, os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# sys.path.append("mma_reach_height/modules/")
from modules.cli_logger import CLILogger

#instantiate cli args and class loggers using cli_logger module
CLILogger('plotter',['Plotter'])
plotterLogger = logging.getLogger('Plotter')

class Plotter:
    def __init__(self, styles, data= None):
        plotterLogger.debug(f'Plotter instantiated')
        self.data = data
        self.style = styles
        # self._win_plot('reach')
        # self._win_plot('height')
        # self._win_type_plot('reach')
        # self._win_type_plot('height')

    def _win_plot(self, reach_height):
        plotterLogger.info(f'plotting {reach_height} wins')
        if reach_height == 'reach':
            wins = self.data['reach_win'].tolist().count(True)
            losses = self.data['reach_win'].tolist().count(False)
            labels = ['Long Reach Wins', 'Short Reach Wins']
        if reach_height == 'height':
            labels = ['Tall Wins', 'Short wins']
            wins = self.data['height_win'].tolist().count(True)
            losses = self.data['height_win'].tolist().count(False)
        data = [float(wins/len(self.data))*100,float(losses/len(self.data))*100]

        fig, ax = plt.subplots(figsize =(10, 7))
        ax.set_title(f"{reach_height.capitalize()} Win-Loss Distribution", fontdict= self.style['title'])
        fig.set_facecolor(self.style['face_color_primary'])
        ax.patch.set_facecolor(self.style['face_color_secondary'])
        ax.grid(color= self.style['grid_color'], linestyle= '--', linewidth=0.7)
        ax.spines['bottom'].set_color(self.style['spline_color'])
        ax.spines['top'].set_color(self.style['spline_color'])
        ax.spines['left'].set_color(self.style['spline_color'])
        ax.spines['right'].set_color(self.style['spline_color'])
        ax.tick_params(colors= self.style['tick_color'])
        ax.tick_params(colors= self.style['tick_color'])

        wedges, texts, autotexts = ax.pie(data,
                                          autopct = '%.1f%%',
                                          labels = labels,
                                          colors = (self.style['red'], self.style['blue']),
                                          startangle = 90,
                                          textprops = dict(
                                              color = self.style['label']['color'],
                                              size= self.style['label']['size']))

        ax.legend(wedges, labels,
                  title =f"{reach_height.capitalize()} Wins-Losses",
                  loc ="upper left",
                  bbox_to_anchor =(1, 0, 0.5, 1))
        plt.setp(autotexts, size = self.style['label']['size'], color= 'white', weight ="bold")

        # plt.savefig(f'mma_reach_height/data_output/{reach_height}_pie')
        plt.savefig(f'data_output/{reach_height}_pie')
        plt.show()

    # #NOT WORKING
    # def _win_type_plot(self, reach_height):
    #     plotterLogger.info(f'plotting {reach_height} win types')
    #     if reach_height == 'reach':
    #         print('reach')
    #         wins = self.data[f'{reach_height}_win'].tolist()
    #     if reach_height == 'height':
    #         wins = self.data[f'{reach_height}_win'].tolist()
    #     win_types = set(self.data['win_type'].tolist())
    #     # print(wins)
    #     wins = self.data[f'{reach_height}_win'].tolist().count(True)
    #     plt.style.use('fast')
    #     plt.figure(figsize=(10,10))
    #     x_pos = [i*2 for i, _ in enumerate(win_types)]
    #     plt.bar(x_pos, wins, width=1)
    #     plt.xlabel('Win Types')
    #     plt.ylabel(f'{reach_height} Wins')
    #     plt.title(f"{reach_height} Wins Per Win Type")
    #     plt.xticks(x_pos, win_types, rotation=45)
    #     plt.tight_layout()
    #     # plt.savefig(f'mma_reach_height/data_output/{reach_height}_wins_per_win_type')
    #     plt.savefig(f'data_output/{reach_height}_wins_per_win_type')

    #     data = set(self.data['win_type'].tolist())
    #     plt.show()