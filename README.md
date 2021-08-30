# MMA Simple Analysis

## Datasets

2 datasets are used, both of which are pulled from Kaggle.com. These datasets provide characteristics about UFC fighters (height, reach, etc.) and betting odds data for individual fights.
* [MMA Fighter Dataset](https://www.kaggle.com/rajeevw/ufcdata)
* [MMA Odds Dataset](https://www.kaggle.com/mdabbert/ufc-fights-2010-2020-with-betting-odds)

## Analysis Outline

For this analysis, we will look into (1) to what degree fighter attributes (height and reach) contribute to match outcome, (2) to what degree do fight these attributes affect different groups (weightclass and gender), and finally (3) to what extent do Vegas odds follow fighter reach?

## Analysis and Conclusion

Basic exploration of the data sets reveal that longer reach and taller height contribute to a slightly higher win percentage. Furthermore, there exists a noticeable difference in the odds distribution between red fighter and blue fighter. Through a scatter plot, we can see that odds favor the red fighter. This can be explained by how the corners are chosen. the colors are seeded as follow Red fighter is the champion or the veteran fighter; blue fighter is the contender or underdog. Lastly, by looking into the mean odds by fighter reach, we can interpret the relationship as follows:
* For the fighter with a reach advantage (i.e. a longer reach), as fighter reach increases, the odds increasingly favor the fighter with a reach advantage
* For the fighter with a reach disadvantage (i.e. a shorter reach), as fighter reach increases, the odds increasingly disfavor the fighter with a reach disadvantage

## Dependencies

To use the virtual env which has all dependencies installed run the following command from inside the project directory: <br />
`source mma-env/bin/activate`

Running the project without the venv will require the following packages:
* numpy
* pandas
* matplotlib

## Running the Project

4 optional flags are available:
* `-v` or `--verbose` Adds verbose logging for fined-grained program logging
* `-o` or `--output` Exports datasets, individual and combined, to CSV
* `-p` or `--prefix` Adds a prefix to all non-essential exported data with simple string
* `-d` or `--dark` Plots output with a dark-mode theme

1 positional arguments required: `command`. Command accepts 1 of 3 options:
* `explore` Plots and outputs data for each individual dataset and analyses
* `analyze` Plots and outputs data for the combined dataset and analyses
* `deep` Plots and outputs data for both individual and combined datasets and analyses

Running the program

`python main.py <command> <optional flags>`

Running unit tests with included test runner

`python3 unit_tests/test_main.py`
