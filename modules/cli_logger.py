### MODULE: responsible for creating dynamic loggers and configuring the cli for each worker module ###
import logging, os ,argparse

class CLILogger:
    def __init__(self,log_name,loggers):
        self.log_lvl = self._cli_config().log_level
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
        parser = argparse.ArgumentParser(description= 'gather and analyze MMA reach and height data', epilog= 'Ready? FIGHT!')
        parser.add_argument('-v', '--verbose', help= 'add logging verbosity', action= 'store_const', dest= 'log_level', const= logging.DEBUG, default= logging.INFO)
        args = parser.parse_args()
        return args
