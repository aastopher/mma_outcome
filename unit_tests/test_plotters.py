import unittest, sys, os
import pandas as pd
sys.path.append("modules/")
from fighter_plotter import Plotter as FPlotter
from odds_plotter import Plotter as OPlotter
from fighter_data_pipe import CalculatedData
from odds_data_pipe import DataLoader

STYLE = {
    'title' : { 'color': '#fefffe', 'weight': 'bold', 'size': 16 },
    'label' : { 'color': '#afb1b6', 'style': 'italic', 'size': 12 },
    'spline_color' : '#32323e',
    'face_color_primary' : '#252429',
    'face_color_secondary' : '#32323e',
    'grid_color' : '#53545f',
    'tick_color' : '#64636b',
    'red' : '#e5383b',
    'blue' : '#5469c4'}

class TestPlotter(unittest.TestCase):

    def test_fighter_plotter(self):
        data = CalculatedData()
        plot = FPlotter(STYLE,data.data)
        plot._create_plots()
        self.assertTrue(len(plot.data['reach_win'].tolist()) > 0)
        self.assertTrue(len(plot.data['height_win'].tolist()) > 0)
        self.assertTrue(len(plot.data['win_type'].tolist()) > 0)
        self.assertTrue(os.path.exists('data_output/reach_pie.png'))
        self.assertTrue(os.path.exists('data_output/height_pie.png'))
        self.assertTrue(os.path.exists('data_output/reach_wins_per_win_type.png'))
        self.assertTrue(os.path.exists('data_output/height_wins_per_win_type.png'))
        os.remove('data_output/reach_pie.png')
        os.remove('data_output/height_pie.png')
        os.remove('data_output/reach_wins_per_win_type.png')
        os.remove('data_output/height_wins_per_win_type.png')

    def test_odds_plotter(self):
        data = DataLoader()
        plot = OPlotter(STYLE,data.data)
        plot._create_plots()
        self.assertTrue(len(plot.data['r_fighter'].tolist()) > 0)
        self.assertTrue(len(plot.data['b_fighter'].tolist()) > 0)
        self.assertTrue(len(plot.data['r_odds'].tolist()) > 0)
        self.assertTrue(len(plot.data['b_odds'].tolist()) > 0)
        self.assertTrue(len(plot.data['gender'].tolist()) > 0)
        self.assertTrue(len(plot.data['winner_resolved'].tolist()) > 0)
        self.assertTrue(len(plot.data['location_resolved'].tolist()) > 0)
        self.assertTrue(os.path.exists('data_output/gender_data.csv'))
        self.assertTrue(os.path.exists('data_output/odds_by_gender_plot.png'))
        os.remove('data_output/gender_data.csv')
        os.remove('data_output/odds_by_gender_plot.png')


if __name__ == '__main__':
    unittest.main()
