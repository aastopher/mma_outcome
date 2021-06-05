from modules.setup import *

# Instantiate cli args
cli = CLILogger('odds_plotter', ['Plotter'])
plotterLogger = logging.getLogger('Plotter')

class Plotter():
    def __init__(self, styles, data):
        self.data = data
        self.style = styles

    def _create_plots(self):
        """ Generate plots and CSV files for analysis. """
        plotterLogger.info('EXECUTING _create_plots()')

        # Convert dataframe to numpy matrix
        plotterLogger.info('Converting data frame to numpy array')
        arr = self.data.to_numpy()

        # Get all row values for r_odds and b_odds
        x = arr[:, 2]
        y = arr[:, 3]

        # Plot histogram
        plotterLogger.info('Setting up plots')
        fig_1, ax_1 = plt.subplots()
        fig_2, ax_2 = plt.subplots(4, 2)
        fig_3, ax_3 = plt.subplots(2, 2)
        fig_1.set_size_inches(13, 10)
        fig_2.set_size_inches(13, 10)
        fig_3.set_size_inches(13, 10)

        # Q1: Do the both fighters have a similar distribution of odds?

        ax_1.set_title('Distribution of Odds by Fighter', fontdict= self.style['title'])
        ax_1.set_xlabel('Fighter Reach (Inches)', fontdict= self.style['label'])
        ax_1.set_ylabel('Vegas Odds', fontdict= self.style['label'])
        fig_1.set_facecolor(self.style['face_color_primary'])
        ax_1.patch.set_facecolor(self.style['face_color_secondary'])
        ax_1.grid(color= self.style['grid_color'], linestyle= '--', linewidth=0.7)
        ax_1.spines['bottom'].set_color(self.style['spline_color'])
        ax_1.spines['top'].set_color(self.style['spline_color'])
        ax_1.spines['left'].set_color(self.style['spline_color'])
        ax_1.spines['right'].set_color(self.style['spline_color'])
        ax_1.tick_params(colors= self.style['tick_color'])
        ax_1.tick_params(colors= self.style['tick_color'])

        plotterLogger.info('Plotting basic histogram of odds')
        ax_1.hist([x, y], bins= 15, color= (self.style['red'], self.style['blue']))

        # Q2: How do odds vary between top weight classes?

        # Get the weight_class array and create boolean masks for each class
        wgt_array = arr[:, 9]
        lw_mask = wgt_array == 'Lightweight'
        ww_mask = wgt_array == 'Welterweight'
        hw_mask = wgt_array == 'Heavyweight'
        lhw_mask = wgt_array == 'Light Heavyweight'

        # Apply the masks to get the odds for each weight class
        w_1 = arr[lw_mask, 2]
        w_2 = arr[lw_mask, 3]
        x_1 = arr[ww_mask, 2]
        x_2 = arr[ww_mask, 3]
        y_1 = arr[lhw_mask, 2]
        y_2 = arr[lhw_mask, 3]
        z_1 = arr[hw_mask, 2]
        z_2 = arr[hw_mask, 3]

        # Setup file output
        weight_df = pd.DataFrame(arr[:, [2, 3, 9]])
        try:
            plotterLogger.info('Writing odds by weight class data')
            weight_df.to_csv(
                path_or_buf= 'data_output/weight_data.csv',
                header= ['r_odds', 'b_odds', 'weight_class'],
                index_label= 'index',
                quoting= csv.QUOTE_NONNUMERIC
            )
        except Exception as err:
            plotterLogger.error(err)

        # Setup plotting
        fig_2.suptitle('Distribution of Odds by Top Weight Class',
            fontweight= self.style['title']['weight'],
            size= self.style['title']['size'],
            color= self.style['title']['color'])
        fig_2.set_facecolor(self.style['face_color_primary'])

        for r, c in ax_2:
            r.set_xlabel('Vegas Odds', fontdict= self.style['label'])
            c.set_xlabel('Vegas Odds', fontdict= self.style['label'])
            r.set_ylabel('Count', fontdict= self.style['label'])
            c.set_ylabel('Count', fontdict= self.style['label'])

            # Set colors
            r.patch.set_facecolor(self.style['face_color_secondary'])
            c.patch.set_facecolor(self.style['face_color_secondary'])
            r.grid(color= self.style['grid_color'], linestyle= '--', linewidth=0.7)
            r.spines['bottom'].set_color(self.style['spline_color'])
            r.spines['top'].set_color(self.style['spline_color'])
            r.spines['left'].set_color(self.style['spline_color'])
            r.spines['right'].set_color(self.style['spline_color'])
            r.tick_params(colors= self.style['tick_color'])
            r.tick_params(colors= self.style['tick_color'])
            c.grid(color= self.style['grid_color'], linestyle= '--', linewidth=0.7)
            c.spines['bottom'].set_color(self.style['spline_color'])
            c.spines['top'].set_color(self.style['spline_color'])
            c.spines['left'].set_color(self.style['spline_color'])
            c.spines['right'].set_color(self.style['spline_color'])
            c.tick_params(colors= self.style['tick_color'])
            c.tick_params(colors= self.style['tick_color'])

        # Set titles
        ax_2[0, 0].set_title('Lightweight Red', fontdict= self.style['label'])
        ax_2[0, 1].set_title('Lightweight Blue', fontdict= self.style['label'])
        ax_2[1, 0].set_title('Welterweight Red', fontdict= self.style['label'])
        ax_2[1, 1].set_title('Welterweight Blue', fontdict= self.style['label'])
        ax_2[2, 0].set_title('Lightweight Heavyweight Blue', fontdict= self.style['label'])
        ax_2[2, 1].set_title('Lightweight Heavyweight Red', fontdict= self.style['label'])
        ax_2[3, 0].set_title('Heavyweight Red', fontdict= self.style['label'])
        ax_2[3, 1].set_title('Heavyweight Blue', fontdict= self.style['label'])

        # Plot
        plotterLogger.info('Plotting histograms of odds by weight classes')
        ax_2[0, 0].hist(w_1, bins= 25, color= self.style['red'])
        ax_2[0, 1].hist(w_2, bins= 25, color= self.style['blue'])
        ax_2[1, 0].hist(x_1, bins= 25, color= self.style['red'])
        ax_2[1, 1].hist(x_2, bins= 25, color= self.style['blue'])
        ax_2[2, 0].hist(y_1, bins= 25, color= self.style['red'])
        ax_2[2, 1].hist(y_2, bins= 25, color= self.style['blue'])
        ax_2[3, 0].hist(z_1, bins= 25, color= self.style['red'])
        ax_2[3, 1].hist(z_2, bins= 25, color= self.style['blue'])

        # Q3: How do the odds vary by gender?

        # Get the gender array and create boolean masks for each gender
        gender_array = arr[:, 10]
        m_mask = gender_array == 'MALE'.lower()
        f_mask = gender_array == 'FEMALE'.lower()

        # Apply the masks to get the odds for each gender
        a_1 = arr[f_mask, 2]
        a_2 = arr[f_mask, 3]
        b_1 = arr[m_mask, 2]
        b_2 = arr[m_mask, 3]

        # Setup file output
        gender_df = pd.DataFrame(arr[:, [2, 3, 10]])
        try:
            plotterLogger.info('Writing odds by gender data')
            gender_df.to_csv(
                path_or_buf= 'data_output/gender_data.csv',
                header= ['r_odds', 'b_odds', 'gender'],
                index_label= 'index',
                quoting= csv.QUOTE_NONNUMERIC
            )
        except Exception as err:
            plotterLogger.error(err)

        # Setup plotting
        fig_3.suptitle('Odds by Gender: Red vs. Blue',
            fontweight= self.style['title']['weight'],
            size= self.style['title']['size'],
            color= self.style['title']['color'])
        fig_3.set_facecolor(self.style['face_color_primary'])

        for r in ax_3:
            r[0].set_xlabel('Vegas Odds', fontdict= self.style['label'])
            r[1].set_xlabel('Vegas Odds', fontdict= self.style['label'])
            r[0].set_ylabel('Count', fontdict= self.style['label'])
            r[1].set_ylabel('Count', fontdict= self.style['label'])

            # Set colors
            r[0].patch.set_facecolor(self.style['face_color_secondary'])
            r[1].patch.set_facecolor(self.style['face_color_secondary'])
            r[0].grid(color= self.style['grid_color'], linestyle= '--', linewidth=0.7)
            r[1].grid(color= self.style['grid_color'], linestyle= '--', linewidth=0.7)
            r[0].spines['bottom'].set_color(self.style['spline_color'])
            r[0].spines['top'].set_color(self.style['spline_color'])
            r[0].spines['left'].set_color(self.style['spline_color'])
            r[0].spines['right'].set_color(self.style['spline_color'])
            r[1].spines['bottom'].set_color(self.style['spline_color'])
            r[1].spines['top'].set_color(self.style['spline_color'])
            r[1].spines['left'].set_color(self.style['spline_color'])
            r[1].spines['right'].set_color(self.style['spline_color'])
            r[0].tick_params(colors= self.style['tick_color'])
            r[1].tick_params(colors= self.style['tick_color'])

        plotterLogger.info('Plotting basic histogram of odds by gender')
        ax_3[0, 0].set_title('Female Red', fontdict= self.style['label'])
        ax_3[0, 1].set_title('Female Blue', fontdict= self.style['label'])
        ax_3[0, 0].hist(a_1, bins= 25, color= self.style['red'])
        ax_3[0, 1].hist(a_2, bins= 25, color= self.style['blue'])
        ax_3[1, 0].set_title('Male Red', fontdict= self.style['label'])
        ax_3[1, 1].set_title('Male Blue', fontdict= self.style['label'])
        ax_3[1, 0].hist(b_1, bins= 25, color= self.style['red'])
        ax_3[1, 1].hist(b_2, bins= 25, color= self.style['blue'])

        # Plot
        fig_1.tight_layout()
        fig_2.tight_layout()
        fig_3.tight_layout()
        plt.savefig(f'data_output/odds_by_gender_plot')
        # plt.show()
