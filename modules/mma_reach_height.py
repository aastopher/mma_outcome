from fighter_data_pipe import *
from fighter_plotter import *

def main():
    data = CalculatedData()
    plot = Plotter(data.data)
    plot._win_plot('reach')
if __name__ == '__main__':
    main()
