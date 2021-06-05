import sys
sys.path.append("modules/")
from setup import *

# Instantiate cli args
cli = CLILogger('odds_data_pipe', ['DataLoader'])
rawDataLogger = logging.getLogger('DataLoader')

IN_DATAFILE_PATH = 'data/raw_odds_details.csv'
class DataLoader:
    def __init__(self):
        self.data = None
        self._load_data()

    def _load_data(self):
        """ Cleanses data generated from Kaggle and writes it to disk. """
        rawDataLogger.info('EXECUTING _load_data()')

        # Ensure we have a file to clean
        try:
            rawDataLogger.info('Reading CSV into Data Frame')
            # Read CSV into Data Frame
            df = pd.read_csv(
                IN_DATAFILE_PATH,
                sep= ',',
                header= 0,
                parse_dates= [4],
                infer_datetime_format= True,
                quotechar= '"',
                encoding= 'utf-8',
                dtype= {
                    'R_fighter': pd.StringDtype(),
                    'B_fighter': pd.StringDtype(),
                    'R_odds': pd.Int16Dtype(),
                    'B_odds': pd.Int16Dtype(),
                    'location': pd.StringDtype(),
                    'country': pd.StringDtype(),
                    'Winner': pd.StringDtype(),
                    'title_bout': pd.StringDtype(),
                    'weight_class': pd.StringDtype(),
                    'gender': pd.StringDtype()
                },
                skip_blank_lines= True
            )

            # Drop NA values
            rawDataLogger.info('Dropping NaN rows')
            df.dropna(how= 'all', inplace= True)

            # Rename our columns for consistency
            rawDataLogger.info('Renaming column headings')
            cols = ['r_fighter', 'b_fighter', 'r_odds', 'b_odds', 'date', 'location', 'country', 'winner', 'title_bout', 'weight_class', 'gender']
            df.columns = cols

            # Add resolved winner column with name
            rawDataLogger.info('Resolving fight winner with fighter name')
            df['winner_resolved'] = [df['r_fighter'] if x.lower() == 'red' else df['b_fighter'] for x in df['winner']]

            # Add resolved country column with country removed from location
            rawDataLogger.info('Resolving location name to split-out country')
            df['location_resolved'] = [x[0:x.rfind(',')].strip() for x in df['location']]

            # Clean string data
            rawDataLogger.info('Converting string columns to lower')
            df['r_fighter'] = df['r_fighter'].str.lower()
            df['b_fighter'] = df['b_fighter'].str.lower()
            df['location_resolved'] = df['location_resolved'].str.lower()
            df['country'] = df['country'].str.lower()
            df['winner_resolved'] = df['winner_resolved'].str.lower()
            df['gender'] = df['gender'].str.lower()

            # Store attributes
            self.data = df
        except OSError as err:
            rawDataLogger.error(f'Exception occurred: {err}')
