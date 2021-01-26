import csv
import matplotlib.pyplot as plt
import pandas as pd

colors = ['red', 'green', 'blue', 'yellow', 'pink', 'black', 'orange',
          'purple', 'brown', 'gray', 'cyan', 'magenta']

pairs = [('Time (mS)', 'Used GR3D (%)')]

class Graph:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file, skiprows=1, header=0, index_col=0)

    def scatter_plot(self, x, y):
        plt.xlabel(x)
        plt.ylabel(y)
        plt.scatter(self.df.loc[:, x], self.df.loc[:, y])
        plt.show()

    def plots(self):
        for pair in pairs:
            self.scatter_plot(pair[0], pair[1])

if __name__ == '__main__':
    csv_file = 'output_log.csv'

    graph = Graph(csv_file)
    graph.plots()
