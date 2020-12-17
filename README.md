# tegrastats_parser

A simple python algorithm to parse Tegrastats data from a log file

Usage
```
python tegrastat.py --log_file <path_to_log_file>/<name_of_log_file>.txt
```

To add a time stamp to your Tegrastats log file, run Tegrastats on your NVIDIA board by executing the following command
```
{ echo $(date -u) & tegrastats --interval <logging_interval_in_mS>; } > <name_of_log_file>.txt
```

To stop running Tegrastats in the background, execute the following command
```
tegrastats --stop
```
