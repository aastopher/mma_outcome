import unittest, sys
sys.path.append("modules/")
from fighter_data_pipe import CalculatedData as FCalculatedData
from odds_data_pipe import DataLoader as ODataLoader

class TestDataPipe(unittest.TestCase):

    def test_fighter_data_pipe(self):
        data = FCalculatedData()
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

    def test_odds_data_pipe(self):
        data = ODataLoader()

if __name__ == '__main__':
    unittest.main()
