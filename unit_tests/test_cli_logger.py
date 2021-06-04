import unittest, sys, os
sys.path.append("mma_reach_height/modules/")
from cli_logger import *

class TestCLI(unittest.TestCase):

    def test_cli(self):
        cli = CLILogger('test_cli_logger',['Class1','Class2','Class3'])
        testLogger1 = logging.getLogger('Class1')
        testLogger1.info('test Class 1')
        testLogger2 = logging.getLogger('Class2')
        testLogger2.info('test Class 2')
        testLogger3 = logging.getLogger('Class3')
        testLogger3.info('test Class 3')
        self.assertTrue(os.path.exists('mma_reach_height/logs/test_cli_logger.log'))
        os.remove('mma_reach_height/logs/test_cli_logger.log')

if __name__ == '__main__':
    unittest.main()
