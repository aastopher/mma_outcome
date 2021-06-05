from fighter_data_pipe import *
from fighter_plotter import *

def main():
    styles = {
                'title' : { 'color': '#fefffe', 'weight': 'bold', 'size': 16 },
                'label' : { 'color': '#afb1b6', 'style': 'italic', 'size': 12 },
                'spline_color' : '#32323e',
                'face_color_primary' : '#252429',
                'face_color_secondary' : '#32323e',
                'grid_color' : '#53545f',
                'tick_color' : '#64636b',
                'red' : '#e5383b',
                'blue' : '#5469c4'
            }
    data = CalculatedData()
    plot = Plotter(styles,data.data)
if __name__ == '__main__':
    main()
