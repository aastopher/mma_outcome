import unittest, sys, os
import pandas as pd
sys.path.append("modules/")
from fighter_plotter import Plotter as FPlotter
from odds_plotter import Plotter as OPlotter

class TestPlotter(unittest.TestCase):

    def test_fighter_plotter(self):
        data = pd.DataFrame({'reach_win':[1,2,3,4,5],'height_win':[1,2,3,4,5],'win_type':['ko','dec','dq','dr','split']})
        plot = FPlotter({},data)
        self.assertTrue(len(plot.data['reach_win'].tolist()) > 0)
        self.assertTrue(len(plot.data['height_win'].tolist()) > 0)
        self.assertTrue(os.path.exists('data_output/reach_pie.png'))
        self.assertTrue(os.path.exists('data_output/height_pie.png'))

    def test_odds_plotter(self):
        something = True
        # data = pd.DataFrame({'reach_win':[1,2,3,4,5],'height_win':[1,2,3,4,5],'win_type':['ko','dec','dq','dr','split']})
        # plot = OPlotter(data)
        # self.assertTrue(len(plot.data['reach_win'].tolist()) > 0)
        # self.assertTrue(len(plot.data['height_win'].tolist()) > 0)
        # self.assertTrue(os.path.exists('mma_reach_height/data_output/reach_pie.png'))
        # self.assertTrue(os.path.exists('mma_reach_height/data_output/height_pie.png'))


if __name__ == '__main__':
    unittest.main()
