import unittest, sys
sys.path.append("mma_reach_height/modules/")
from data_pipe import *

class TestDataPipe(unittest.TestCase):

    def test_data_pipe(self):
        data = CalculatedData()
        self.assertTrue(data.reach_win_percentage > 0)
        self.assertTrue(data.height_win_percentage > 0)
        self.assertTrue(data.data['r_fighter'].count().sum()>0)
        self.assertTrue(data.data['r_reach'].count().sum()>0)
        self.assertTrue(data.data['r_height'].count().sum()>0)
        self.assertTrue(data.data['b_fighter'].count().sum()>0)
        self.assertTrue(data.data['b_reach'].count().sum()>0)
        self.assertTrue(data.data['b_height'].count().sum()>0)
        self.assertTrue(data.data['win_type'].count().sum()>0)
        self.assertTrue(data.data['last_round'].count().sum()>0)
        self.assertTrue(data.data['match_type'].count().sum()>0)
        self.assertTrue(data.data['match_length'].count().sum()>0)
        self.assertTrue(data.data['referee'].count().sum()>0)
        self.assertTrue(data.data['date'].count().sum()>0)
        self.assertTrue(data.data['winner'].count().sum()>0)
        self.assertTrue(data.data['reach_win'].count().sum()>0)
        self.assertTrue(data.data['height_win'].count().sum()>0)

if __name__ == '__main__':
    unittest.main()
