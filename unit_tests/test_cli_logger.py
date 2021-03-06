import unittest, sys, os, argparse
sys.path.append("modules/")
from cli_logger import *

class TestCLI(unittest.TestCase):

    def test_logger(self):
        cli = CLILogger('test_cli_logger',['Class1','Class2','Class3'])
        testLogger1 = logging.getLogger('Class1')
        testLogger1.info('test Class 1')
        testLogger2 = logging.getLogger('Class2')
        testLogger2.info('test Class 2')
        testLogger3 = logging.getLogger('Class3')
        testLogger3.info('test Class 3')
        self.assertTrue(os.path.exists('logs/test_cli_logger.log'))
        os.remove('logs/test_cli_logger.log')

    def test_cli(self):
        cli = CLILogger('test_cli_logger',['Class1','Class2','Class3'])

        #test explore command combinations
        args = cli.parser.parse_args(['explore'])
        self.assertTrue(args.command == 'explore')
        self.assertTrue(args.log_level == 20)
        self.assertTrue(args.dark_mode == False)
        self.assertTrue(args.prefix == [''])
        self.assertTrue(args.output == False)
        args = cli.parser.parse_args(['explore','-v'])
        self.assertTrue(args.command == 'explore')
        self.assertTrue(args.log_level == 10)
        self.assertTrue(args.dark_mode == False)
        self.assertTrue(args.prefix == [''])
        self.assertTrue(args.output == False)
        args = cli.parser.parse_args(['explore','-v','-d'])
        self.assertTrue(args.command == 'explore')
        self.assertTrue(args.log_level == 10)
        self.assertTrue(args.dark_mode == True)
        self.assertTrue(args.prefix == [''])
        self.assertTrue(args.output == False)
        args = cli.parser.parse_args(['explore','-v','-d','-p','test'])
        self.assertTrue(args.command == 'explore')
        self.assertTrue(args.log_level == 10)
        self.assertTrue(args.dark_mode == True)
        self.assertTrue(args.prefix == ['test'])
        self.assertTrue(args.output == False)
        args = cli.parser.parse_args(['explore','-v','-d','-p','test','-o'])
        self.assertTrue(args.command == 'explore')
        self.assertTrue(args.log_level == 10)
        self.assertTrue(args.dark_mode == True)
        self.assertTrue(args.prefix == ['test'])
        self.assertTrue(args.output == True)

        #test analyze command combinations
        args = cli.parser.parse_args(['analyze'])
        self.assertTrue(args.command == 'analyze')
        self.assertTrue(args.log_level == 20)
        self.assertTrue(args.dark_mode == False)
        self.assertTrue(args.prefix == [''])
        self.assertTrue(args.output == False)
        args = cli.parser.parse_args(['analyze','-v'])
        self.assertTrue(args.command == 'analyze')
        self.assertTrue(args.log_level == 10)
        self.assertTrue(args.dark_mode == False)
        self.assertTrue(args.prefix == [''])
        self.assertTrue(args.output == False)
        args = cli.parser.parse_args(['analyze','-v','-d'])
        self.assertTrue(args.command == 'analyze')
        self.assertTrue(args.log_level == 10)
        self.assertTrue(args.dark_mode == True)
        self.assertTrue(args.prefix == [''])
        self.assertTrue(args.output == False)
        args = cli.parser.parse_args(['analyze','-v','-d','-p','test'])
        self.assertTrue(args.command == 'analyze')
        self.assertTrue(args.log_level == 10)
        self.assertTrue(args.dark_mode == True)
        self.assertTrue(args.prefix == ['test'])
        self.assertTrue(args.output == False)
        args = cli.parser.parse_args(['analyze','-v','-d','-p','test','-o'])
        self.assertTrue(args.command == 'analyze')
        self.assertTrue(args.log_level == 10)
        self.assertTrue(args.dark_mode == True)
        self.assertTrue(args.prefix == ['test'])
        self.assertTrue(args.output == True)

        #test deep command combinations
        args = cli.parser.parse_args(['deep'])
        self.assertTrue(args.command == 'deep')
        self.assertTrue(args.log_level == 20)
        self.assertTrue(args.dark_mode == False)
        self.assertTrue(args.prefix == [''])
        self.assertTrue(args.output == False)
        args = cli.parser.parse_args(['deep','-v'])
        self.assertTrue(args.command == 'deep')
        self.assertTrue(args.log_level == 10)
        self.assertTrue(args.dark_mode == False)
        self.assertTrue(args.prefix == [''])
        self.assertTrue(args.output == False)
        args = cli.parser.parse_args(['deep','-v','-d'])
        self.assertTrue(args.command == 'deep')
        self.assertTrue(args.log_level == 10)
        self.assertTrue(args.dark_mode == True)
        self.assertTrue(args.prefix == [''])
        self.assertTrue(args.output == False)
        args = cli.parser.parse_args(['deep','-v','-d','-p','test'])
        self.assertTrue(args.command == 'deep')
        self.assertTrue(args.log_level == 10)
        self.assertTrue(args.dark_mode == True)
        self.assertTrue(args.prefix == ['test'])
        self.assertTrue(args.output == False)
        args = cli.parser.parse_args(['deep','-v','-d','-p','test','-o'])
        self.assertTrue(args.command == 'deep')
        self.assertTrue(args.log_level == 10)
        self.assertTrue(args.dark_mode == True)
        self.assertTrue(args.prefix == ['test'])
        self.assertTrue(args.output == True)

if __name__ == '__main__':
    unittest.main()
