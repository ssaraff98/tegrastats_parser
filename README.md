# tegrastats_parser

A simple python algorithm to run Tegrastats and then parse data from the time-stamped log file obtained.

Usage
```
python main.py --interval <logging_interval_in_mS> --log_file <path_to_log_file>/<name_of_log_file>.txt
```
Command line options:
1. --interval, -i   (type=int, default=1000, help='Logging interval in milliseconds for tegrastats')
2. --log_file, -f   (type=string, default='output_log.txt', help='Log file name for tegrastats data')
3. --only_parse, -p (help='Parse tegrastats log file without running tegrastats')
4. --graph, -g      (help='Plots some useful graphs from tegrastats data parsed')

To stop running Tegrastats in the background and parse the log file, execute the following command
```
exit
```

To install all dependency libraries, execute the following command
```
pip3 install -r requirements.txt
```
