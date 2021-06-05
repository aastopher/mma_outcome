### MODULE: responsible for creating dynamic loggers and configuring a cli ###
import logging, os ,argparse

class CLILogger:
    def __init__(self,log_name,loggers):
        self.args,self.parser = self._cli_config()
        if not self.args.command:
            self.log_lvl = logging.INFO
        else:
            self.log_lvl = self.args.log_level
        self.loggers = loggers
        self.log_name = log_name
        self._logging_config()
    def _logging_config(self):
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        if not os.path.exists('logs'):
            os.mkdir('logs')
        fh = logging.FileHandler(f'logs/{self.log_name}.log','w')
        fh.setLevel(self.log_lvl)
        formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
        fh.setFormatter(formatter)
        for log in self.loggers:
            logger = logging.getLogger(f'{log}')
            logger.addHandler(fh)
        infoLogger = logging.getLogger('console')
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        infoLogger.addHandler(sh)
    def _cli_config(self):
        def _add_options(parser):
            parser.add_argument('-v', '--verbose', help= 'add logging verbosity', action= 'store_const', dest= 'log_level', const= logging.DEBUG, default= logging.INFO)
            parser.add_argument('-d', '--dark-mode', help= 'add dark mode to plotting', action= 'store_true', dest= 'dark_mode')
            parser.add_argument('-o', '--output', help= 'define a prefix for all export data', dest= 'output', nargs=1, default=[''])

        parser = argparse.ArgumentParser(description= f'gather and analyze MMA fight and odds data', epilog= 'Ready? FIGHT!')
        # parser.add_argument('-v', '--verbose', help= 'add logging verbosity', action= 'store_const', dest= 'log_level', const= logging.DEBUG, default= logging.INFO)
        subparser = parser.add_subparsers(dest='command')

        explore_command = subparser.add_parser('explore')
        explore_command.add_argument('explore', help='explore initial dataset plots', action= 'store_true')
        _add_options(explore_command)

        analyze_command = subparser.add_parser('analyze')
        analyze_command.add_argument('analyze', help='explore final analysis plots', action= 'store_true')
        _add_options(analyze_command)

        deep_command = subparser.add_parser('deep')
        deep_command.add_argument('deep', help='explore all data and plots', action= 'store_true')
        _add_options(deep_command)

        return parser.parse_args(), parser
