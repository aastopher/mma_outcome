### MODULE: responsible for all plotting functions ###
import sys
sys.path.append("modules/")
from setup import *

# instantiate cli args and class loggers using cli_logger module
cli = CLILogger('fighter_plotter',['Plotter'])
plotterLogger = logging.getLogger('Plotter')

# set prefix correctly if empty
if cli.args.command == None or cli.args.prefix[0] == '':
    prefix = ''
else:
    prefix = cli.args.prefix[0] + '_'
    plotterLogger.debug(f'Prefix \'{prefix}\' added to output files')

class Plotter:
    def __init__(self, styles, data=None):
        plotterLogger.debug(f'Plotter instantiated')
        self.data = data
        self.style = styles
        self.win_types = set(self.data['win_type'].tolist())
        self.r_win_type_wins = self._win_type_wins('reach')
        self.h_win_type_wins = self._win_type_wins('height')
    def _create_plots(self):
        plotterLogger.info('Creating plots')
        self._win_plot('reach')
        self._win_plot('height')
        self._win_type_plot('reach')
        self._win_type_plot('height')
    def _win_plot(self, reach_height):
        plotterLogger.info(f'Plotting {reach_height} wins')
        plotterLogger.debug(f'Collecting data: {reach_height} pie plot')
        if reach_height == 'reach':
            wins = self.data['reach_win'].tolist().count(True)
            losses = self.data['reach_win'].tolist().count(False)
            labels = ['Long Reach Wins', 'Short Reach Wins']
        if reach_height == 'height':
            labels = ['Tall Wins', 'Short wins']
            wins = self.data['height_win'].tolist().count(True)
            losses = self.data['height_win'].tolist().count(False)
        data = [float(wins/len(self.data))*100,float(losses/len(self.data))*100]

        # setup plot attributes
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

        # create plot
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

        plt.savefig(f'data_output/{prefix}{reach_height}_pie')
        # plt.show()
    def _win_type_plot(self, reach_height):
        plotterLogger.info(f'Plotting {reach_height} win types')
        if reach_height == 'reach':
            wins = self.r_win_type_wins.loc[0].tolist()
        if reach_height == 'height':
            wins = self.h_win_type_wins.loc[0].tolist()
        x_pos = [i*2 for i, _ in enumerate(self.win_types)]

        # setup plot attributes
        fig, ax = plt.subplots(figsize =(10, 10))
        ax.patch.set_facecolor(self.style['face_color_secondary'])
        fig.set_facecolor(self.style['face_color_primary'])
        ax.grid(color= self.style['grid_color'], linestyle= '--', linewidth=0.7)
        ax.tick_params(colors= self.style['tick_color'])

        # create plot
        plt.bar(x_pos, wins, width=1,color=self.style['blue'])
        plt.xlabel('Win Types', fontdict= self.style['label'])
        plt.ylabel(f'{reach_height.capitalize()} Wins', fontdict= self.style['label'])
        plt.title(f"{reach_height.capitalize()} Wins Per Win Type", fontdict= self.style['title'])
        plt.xticks(x_pos, self.win_types, rotation=45)
        plt.tight_layout()

        plt.savefig(f'data_output/{prefix}{reach_height}_wins_per_win_type')
        # plt.show()
    # data collection function for win type bar plots
    def _win_type_wins(self, reach_height):
        plotterLogger.debug(f'Collecting data: {reach_height} bar plot')
        win_type_wins = pd.DataFrame(columns = set(self.data['win_type'].tolist()))
        for type in self.win_types:
            type_indexs = self.data.index[self.data['win_type'] == type].tolist()
            num_wins = [self.data.iloc[i][f'{reach_height}_win'] for i in type_indexs if self.data.iloc[i][f'{reach_height}_win'] == True and self.data.iloc[i]['win_type'] == type]
            self.data.index[self.data[f'{reach_height}_win'] == True].tolist()
            win_type_wins[type] = [np.count_nonzero(num_wins)]
        return win_type_wins
