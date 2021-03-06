### MODULE: responsible for all data handling ###
import sys
sys.path.append("modules/")
from setup import *

# instantiate cli args and class loggers using cli_logger module
cli = CLILogger('fighter_data_pipe',['RawData','ProcessedData','CalculatedData'])
rawDataLogger = logging.getLogger('RawData')
processedDataLogger = logging.getLogger('ProcessedData')
calculatedDataLogger = logging.getLogger('CalculatedData')
infoLogger = logging.getLogger('console')

# Set output correctly if empty
if cli.args.command == None or cli.args.output == False:
    output = False
else:
    output = cli.args.output

# instantiate static vars
MONTH_NUMS = {'january':'01','february':'02','march':'03','april':'04','may':'05','june':'06','july':'07','august':'08','september':'09','october':'10','november':'11','december':'12'}

class RawData:
    def __init__(self):
        rawDataLogger.debug(f'RawData instantiated')
        self.fighters = []
        self.matches = []
        if os.path.exists('data/raw_fighter_details.csv'):
            rawDataLogger.info('Parsing raw data')
            self._load_fighters()
            self._load_matches()
    def _load_fighters(self):
        try:
            rawDataLogger.debug('\'raw_fighter_details.csv\' exists')
            rawDataLogger.debug('Parsing \'raw_fighter_details.csv\' into Fighter DataFrame')
            f = pd.read_csv('data/raw_fighter_details.csv',header=None,skiprows=[0])
            for i in range(len(f)):
                if not pd.isna(f[3][i]) and not pd.isna(f[1][i]):
                    name = (f[0][i]).lower()
                    reach = int(str(f[3][i]).replace('"',''))
                    height = str(f[1][i]).replace('"', "").replace('\'', "'").replace(' ', "")
                    self.fighters.append((name,reach,height))
            self.fighters = pd.DataFrame(self.fighters, columns = ['name','reach','height'])
            self.fighters = self.fighters.set_index('name')
            return self
        except OSError:
            rawDataLogger.debug('\'raw_fighter_details.csv\' could not be loaded')
        return self
    def _load_matches(self):
        try:
            rawDataLogger.debug('\'raw_total_fight_data.csv\' exists')
            rawDataLogger.debug('Parsing \'raw_total_fight_data.csv\' into Match DataFrame')
            f = pd.read_csv('data/raw_total_fight_data.csv',header=None,skiprows=[0])
            for i in range(len(f)):
                r_fighter = f[0][i].split(';')[0].lower()
                b_fighter = f[0][i].split(';')[1].lower()
                win_type = f[0][i].split(';')[32].lower()
                last_round = f[0][i].split(';')[33]
                match_type = f[0][i].split(';')[35].lower()
                referee = f[0][6].split(';')[-2].lower()
                date = f[1][i].split(';')[0].strip() + '-' + MONTH_NUMS[f[0][i].split(';')[37].split(' ')[0].lower()] + '-' + f[0][i].split(';')[37][-2:]
                #if not 3 or 5 round match_type to grab time directly without calculations
                if match_type[0] == '3' or match_type[0] == '5':
                    if int((5*int(f[0][i].split(';')[33]))-(5-int(f[0][i].split(';')[34][0]))) >= 10:
                        match_length = '00:' + str((5*int(f[0][i].split(';')[33]))-(5-int(f[0][i].split(';')[34][0]))) + ':' + f[0][i].split(';')[34].split(':')[1]
                    else:
                        match_length = '00:0' + str((5*int(f[0][i].split(';')[33]))-(5-int(f[0][i].split(';')[34][0]))) + ':' + f[0][i].split(';')[34].split(':')[1]
                else:
                    match_length = f[0][i].split(';')[34]
                #grab correct column if the last column shifts
                if pd.isna(f[3][i]) and f[2][i].split(';')[2]:
                    winner = f[2][i].split(';')[2].lower()
                if not pd.isna(f[3][i]) and f[3][i].split(';')[2]:
                    winner = f[3][i].split(';')[2].lower()
                #only add matches if both fighters exist in fighters dataframe
                if r_fighter in self.fighters.index and b_fighter in self.fighters.index:
                    self.matches.append((r_fighter,b_fighter,win_type,last_round,match_type,match_length,referee,date,winner))
            self.matches = pd.DataFrame(self.matches, columns = ['r_fighter','b_fighter','win_type','last_round','match_type','match_length','referee','date','winner'])
            return self
        except OSError:
            rawDataLogger.debug('\'raw_total_fight_data.csv\' could not be loaded')
        return self

class ProcessedData:
    def __init__(self):
        processedDataLogger.debug(f'ProcessedData instantiated')
        self.reach_outcome = []
        self.height_outcome = []
        self.raw_data = RawData()
        self.data = pd.DataFrame(self.raw_data.matches, columns = ['r_fighter','r_reach','r_height','b_fighter','b_reach','b_height','win_type','last_round','match_type','match_length','referee','date','winner','reach_win','height_win'])
        self._pre_proc_data()
        self._generate_reach_outcome()
        self._generate_height_outcome()
        if os.path.exists('data/raw_fighter_details.csv') and os.path.exists('data/raw_total_fight_data.csv') and not os.path.exists('data_output/processed_data.csv'):
            if not os.path.exists('data_output'):
                processedDataLogger.debug('Creating data_output directory')
                os.mkdir('data_output')
            if output:
                processedDataLogger.debug('Writing \'proccessed_data.csv\'')
                self.data.to_csv(f'data_output/processed_data.csv')
    def _pre_proc_data(self):
        processedDataLogger.info('Pre-processing data for generated results')
        r_reach,r_height = [],[]
        b_reach,b_height = [],[]
        #add reach and height for each fighter to the processed dataframe
        for i in range(len(self.raw_data.matches)):
            r_reach.append(self.raw_data.fighters.loc[self.raw_data.matches['r_fighter'][i]][0])
            r_height.append(self.raw_data.fighters.loc[self.raw_data.matches['r_fighter'][i]][1])
            b_reach.append(self.raw_data.fighters.loc[self.raw_data.matches['b_fighter'][i]][0])
            b_height.append(self.raw_data.fighters.loc[self.raw_data.matches['b_fighter'][i]][1])
        self.data['r_reach'],self.data['r_height'] = r_reach,r_height
        self.data['b_reach'],self.data['b_height'] = b_reach,b_height
        return self
    def _generate_reach_outcome(self):
        processedDataLogger.info('Generating reach outcomes')
        for i in range(len(self.raw_data.matches)):
            r_fighter = (self.raw_data.matches['r_fighter'][i],self.raw_data.fighters.loc[str(self.raw_data.matches['r_fighter'][i])][0])
            b_fighter = (self.raw_data.matches['b_fighter'][i],self.raw_data.fighters.loc[str(self.raw_data.matches['b_fighter'][i])][0])
            if max(r_fighter[1],b_fighter[1]) == r_fighter[1]:
                longer_reach = r_fighter
            else:
                longer_reach = b_fighter
            if longer_reach[0] == self.raw_data.matches['winner'][i]:
                self.reach_outcome.append(True)
            else:
                self.reach_outcome.append(False)
        self.data['reach_win'] = self.reach_outcome
        return self
    def _generate_height_outcome(self):
        processedDataLogger.info('Generating height outcomes')
        for i in range(len(self.raw_data.matches)):
            r_fighter = (self.raw_data.matches['r_fighter'][i],self.raw_data.fighters.loc[str(self.raw_data.matches['r_fighter'][i])][1])
            b_fighter = (self.raw_data.matches['b_fighter'][i],self.raw_data.fighters.loc[str(self.raw_data.matches['b_fighter'][i])][1])
            r_height = int(r_fighter[1].split('\'')[0])+(float(r_fighter[1].split('\'')[1])*.1)
            b_height = int(b_fighter[1].split('\'')[0])+(float(b_fighter[1].split('\'')[1])*.1)
            if max(r_height,b_height) == r_height:
                taller = r_fighter
            else:
                taller = b_fighter
            if taller[0] == self.raw_data.matches['winner'][i]:
                self.height_outcome.append(True)
            else:
                self.height_outcome.append(False)
        self.data['height_win'] = self.height_outcome
        return self

class CalculatedData:
    def __init__(self):
        calculatedDataLogger.debug(f'CalculatedData instantiated')
        self.reach_win_percentage = None
        self.height_win_percentage = None
        try:
            if os.path.exists('data_output/processed_data.csv'):
                self.data = pd.read_csv('data_output/processed_data.csv',header=None,skiprows=[0],names=['r_fighter','r_reach','r_height','b_fighter','b_reach','b_height','win_type','last_round','match_type','match_length','referee','date','winner','reach_win','height_win'])
                calculatedDataLogger.info('Loaded existing processed_data')
            else:
                self.data = ProcessedData().data
                calculatedDataLogger.info('Processed raw_data')
            if np.sum(np.count_nonzero(self.data['reach_win']))>0 and np.sum(np.count_nonzero(self.data['height_win']))>0:
                calculatedDataLogger.debug('Calculating reach and height win percentage')
                self.reach_win_percentage = np.round_(np.sum(self.data['reach_win'].tolist())/len(self.data)*100, decimals = 2)
                self.height_win_percentage = np.round_(np.sum(self.data['height_win'].tolist())/len(self.data)*100,decimals = 2)
            else:
                raise FileNotFoundError
        except FileNotFoundError as err:
            infoLogger.error('MISSING FILE: unable to perform calculations')
