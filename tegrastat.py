###### Tegrastat log file parser ######

import argparse
import csv
import os
import re

# Sample output
# RAM 1404/7860MB (lfb 236x4MB) SWAP 0/3930MB (cached 0MB) CPU [0%@345,0%@960,0%@960,0%@345,0%@345,0%@345]
# EMC_FREQ 0% GR3D_FREQ 0% PLL@35.5C MCPU@35.5C PMIC@100C Tboard@30C GPU@32C BCPU@35.5C thermal@34.1C Tdiode@31.5C
# VDD_SYS_GPU 153/153 VDD_SYS_SOC 306/306 VDD_4V0_WIFI 0/0 VDD_IN 1649/1649 VDD_SYS_CPU 306/306 VDD_SYS_DDR 173/173

class Tegrastat:
    def __init__(self):
        self.header = ["RAM (MB)", "SWAP (MB)", "CPU (%) / FREQ (MHz)", "EMC FREQ (%)",
                       "GR3D FREQ (%)", "PLL (C)", "MCPU (C)", "PMIC (C)", "Tboard (C)",
                       "GPU (C)", "BCPU (C)", "Thermal (C)", "Tdiode (C)", "VDD SYS GPU",
                       "VDD SYS SOC", "VDD 4V0 WIFI", "VDD IN", "VDD SYS CPU", "VDD SYS DDR"]

    def parse_data(self, i, line):
        ram_pattern = r'RAM ([0-9]*)\/([0-9]*)MB'
        swap_pattern = r'SWAP ([0-9]*)\/([0-9]*)MB'
        cpu_pattern = r'[0-9]%@[0-9]*'
        emc_pattern = r'EMC_FREQ ([0-9]*)%'
        gr3d_pattern = r'GR3D_FREQ ([0-9]*)%'
        pll_pattern = r'PLL@([0-9]*[.]{0,1}[0-9]*)C'
        mcpu_pattern = r'MCPU@([0-9]*[.]{0,1}[0-9]*)C'
        pmic_pattern = r'PMIC@([0-9]*[.]{0,1}[0-9]*)C'
        tboad_pattern = r'Tboard@([0-9]*[.]{0,1}[0-9]*)C'

        ram = re.search(ram_pattern, line).group(0)
        swap = re.search(swap_pattern, line).group(0)
        cpu = re.findall(cpu_pattern, line)
        emc = re.findall(emc_pattern, line)
        gr3d = re.findall(gr3d_pattern, line)
        pll = re.findall(pll_pattern, line)
        mcpu = re.findall(mcpu_pattern, line)
        pmic = re.findall(pmic_pattern, line)
        tboard = re.findall(tboad_pattern, line)

        print(ram)
        print(swap)
        print(cpu)
        print(emc)
        print(gr3d)
        print(pll)
        print(mcpu)
        print(pmic)
        print(tboard)

    def parse_file(self, log_file):
        if not os.path.exists(log_file):
            print("Path to file is invalid")
            return

        csv_file = os.path.splitext(log_file)[0] + '.csv'
        # writer = csv.writer(csv_file, delimiter='|')
        # writer.writerows(self.header)

        with open(log_file, 'r') as fopen:
            data = fopen.readlines()

            for i, line in enumerate(data):
                row = self.parse_data(i, line)
                # writer.writerows(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_file', '-i', help='input log file')
    options = parser.parse_args()

    tegrastat = Tegrastat()
    tegrastat.parse_file(options.log_file)
