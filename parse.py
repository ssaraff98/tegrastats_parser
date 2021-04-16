import csv
import os
import re

from icecream import ic #debugging

class Parse:
    def __init__(self, interval, log_file):
        self.interval = int(interval)
        self.log_file = log_file

    def parse_ram(self, lookup_table, ram):
        lookup_table['Used RAM (MB)'] = float(ram[0])
        lookup_table['Total RAM (MB)'] = float(ram[1])
        lookup_table['Number of Free RAM Blocks'] = float(ram[2])
        lookup_table['Size of Free RAM Blocks (MB)'] = float(ram[3])
        return lookup_table

    def parse_swap(self, lookup_table, swap):
        lookup_table['Used SWAP (MB)'] = float(swap[0])
        lookup_table['Total SWAP (MB)'] = float(swap[1])
        lookup_table['Cached SWAP (MB)'] = float(swap[2])
        return lookup_table

    def parse_iram(self, lookup_table, iram):
        lookup_table['Used IRAM (kB)'] = float(iram[0])
        lookup_table['Total IRAM (kB)'] = float(iram[1])
        lookup_table['Size of IRAM Blocks (kB)'] = float(iram[2])
        return lookup_table

    def parse_cpus(self, lookup_table, cpus):
        frequency = re.findall(r'@([0-9]*)', cpus)
        lookup_table['CPU Frequency (MHz)'] = float(frequency[0]) if frequency else ''
        for i, cpu in enumerate(cpus.split(',')):
            lookup_table[f'CPU {i} Load (%)'] = cpu.split('%')[0]
        return lookup_table

    def parse_gr3d(self, lookup_table, gr3d):
        lookup_table['Used GR3D (%)'] = float(gr3d[0])
        lookup_table['GR3D Frequency (MHz)'] = float(gr3d[1]) if gr3d[1] else ''
        return lookup_table

    def parse_emc(self, lookup_table, emc):
        lookup_table['Used EMC (%)'] = float(emc[0])
        lookup_table['GR3D Frequency (MHz)'] = float(emc[1])  if emc[1] else ''
        return lookup_table

    def parse_temperatures(self, lookup_table, temperatures):
        for label, temperature in temperatures:
            lookup_table[f'{label} Temperature (C)'] = float(temperature)
        return lookup_table

    def parse_vdds(self, lookup_table, vdds):
        for label, curr_vdd, avg_vdd in vdds:
            lookup_table[f'Current {label} Power Consumption (mW)'] = float(curr_vdd)
            lookup_table[f'Average {label} Power Consumption (mW)'] = float(avg_vdd)
        return lookup_table

    def parse_data(self, line):
        lookup_table = {}

        ram = re.findall(r'RAM ([0-9]*)\/([0-9]*)MB \(lfb ([0-9]*)x([0-9]*)MB\)', line)
        self.parse_ram(lookup_table, ram[0]) if ram else None

        swap = re.findall(r'SWAP ([0-9]*)\/([0-9]*)MB \(cached ([0-9]*)MB\)', line)
        self.parse_swap(lookup_table, swap[0]) if swap else None

        iram = re.findall(r'IRAM ([0-9]*)\/([0-9]*)kB \(lfb ([0-9]*)kB\)', line)
        self.parse_iram(lookup_table, iram[0]) if iram else None

        cpus = re.findall(r'CPU \[(.*)\]', line)
        self.parse_cpus(lookup_table, cpus[0]) if cpus else None

        ape = re.findall(r'APE ([0-9]*)', line)
        if ape:
            lookup_table['APE frequency (MHz)'] = float(ape[0])

        gr3d = re.findall(r'GR3D_FREQ ([0-9]*)%@?([0-9]*)?', line)
        self.parse_gr3d(lookup_table, gr3d[0]) if gr3d else None

        emc = re.findall(r'EMC_FREQ ([0-9]*)%@?([0-9]*)?', line)
        self.parse_emc(lookup_table, emc[0]) if emc else None

        nvenc = re.findall(r'NVENC ([0-9]*)', line)
        if nvenc:
            lookup_table['NVENC frequency (MHz)'] = float(nvenc[0])

        mts = re.findall(r'MTS fg ([0-9]*)% bg ([0-9]*)%', line) # !!!!

        temperatures = re.findall(r'([A-Za-z]*)@([0-9.]*)C', line)
        vdds = None

        if temperatures:
            self.parse_temperatures(lookup_table, temperatures)
            substring = line[(line.rindex(temperatures[-1][1] + "C") + len(temperatures[-1][1] + "C")):]

            vdds = re.findall(r'([A-Za-z0-9_]*) ([0-9]*)\/([0-9]*)', substring)

        else:
            vdds = re.findall(r'VDD_([A-Za-z0-9_]*) ([0-9]*)\/([0-9]*)', line)
        self.parse_vdds(lookup_table, vdds) if vdds else None

        return lookup_table

    def create_header(self, line):
        labels = ['Index', 'Time (mS)'] + list(self.parse_data(line).keys())
        return labels

    def parse_file(self):
        if not os.path.exists(self.log_file):
            print('Path to log file is invalid\n')
            return

        csv_file = os.path.splitext(self.log_file)[0] + '.csv'

        with open(csv_file, 'w', newline='') as fopen:
            writer = csv.writer(fopen)

            with open(self.log_file, 'r') as log:
                data = log.readlines()
                writer.writerow([data[0]])
                labels = self.create_header(data[1])
                writer.writerow(labels)
                time = 0

                for i, line in enumerate(data[1:]):
                    row = [i, time] + list(self.parse_data(line).values())
                    writer.writerow(row)
                    time = time + self.interval

        return csv_file

if __name__ == '__main__':
    interval = 1000
    log_file = 'output_log.txt'

    parser = Parse(interval, log_file)
    parser.parse_file()
