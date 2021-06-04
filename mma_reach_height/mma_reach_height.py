from modules.data_pipe import *
from modules.plotter import *


def main():
    data = CalculatedData()
    plot = Plotter(data.data)

if __name__ == '__main__':
    main()
