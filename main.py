import argparse
from tegrastats import Tegrastats
from parse import Parse
from graph import Graph

if __name__ == '__main__':
    # Command line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--interval', '-i', type=int, default=1000, help='Logging interval in milliseconds for tegrastats')
    parser.add_argument('--log_file', '-f', default='output_log.txt', help='Log file name for tegrastats data')
    parser.add_argument('--verbose', '-v', action='store_true', help='Prints verbose messages while running tegrastats')
    parser.add_argument('--only_parse', '-p', action='store_true', help='Parse tegrastats log file without running tegrastats')
    parser.add_argument('--graph', '-g', action='store_true', help='Plots some useful graphs from tegrastats data parsed')
    options = parser.parse_args()

    tegrastats = Tegrastats(options.interval, options.log_file, options.verbose)
    parser = Parse(options.interval, options.log_file)

    if not options.only_parse:
        status = tegrastats.run()

    csv_file = parser.parse_file()

    if options.graph:
        graph = Graph(csv_file)
        graph.plots()
