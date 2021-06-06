# MMA Analysis Project

## Datasets

2 datasets are used, both of which are pulled from Kaggle.com. These datasets provide characteristics about UFC fighters (height, reach, etc.) and betting odds data for individual fights.
* [MMA Fighter Dataset](https://www.kaggle.com/rajeevw/ufcdata)
* [MMA Odds Dataset](https://www.kaggle.com/mdabbert/ufc-fights-2010-2020-with-betting-odds)

## Research Question

For this analysis, we will look into (1) to what degree fighter attributes (height and reach) contribute to match outcome, (2) to what degree do fight characteristics (top weightclass and gender) contribute to match outcome, and finally (3) to what extent do Vegas odds follow fighter reach?

## Analysis and Conclusion

Through the analysis, we found that longer reach and and taller height contribute to a higher win percentage. Furthermore, we found that there exists a marked difference in the odds distribution between red fighter and blue fighter. Through a scatterplot, we can see that odds favor the red fighter with the blue fighter being the "underdog" when analyzing on the fighter's reach. Lastly, by looking into the mean odds by fighter reach, we found that there are a few relationships of note:
* For the fighter with a reach advantage (i.e. a longer reach), as fighter reach increases, the odds increasingly favor the fighter with a reach advantage
* For the fighter with a reach disadvantage (i.e. a shorter reach), as fighter reach increases, the odds increasingly disfavor the fighter with a reach disadvantage

## Installation of Packages

The following custom libraries are required for the project to run:
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
