import unittest, sys, os
import pandas as pd
sys.path.append("modules/")
from plotter import *

class TestPlotter(unittest.TestCase):

    def test_plotter(self):
        data = pd.DataFrame({'reach_win':[1,2,3,4,5],'height_win':[1,2,3,4,5]})
        plot = Plotter(data)
        self.assertTrue(len(plot.data['reach_win'].tolist()) > 0)
        self.assertTrue(len(plot.data['height_win'].tolist()) > 0)
        self.assertTrue(os.path.exists('data_output/reach_pie.png'))
        self.assertTrue(os.path.exists('data_output/height_pie.png'))


if __name__ == '__main__':
    unittest.main()
