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
        ram = re.findall(r'RAM ([0-9]*)\/([0-9]*)MB', line)[0]
        swap = re.findall(r'SWAP ([0-9]*)\/([0-9]*)MB', line)[0]
        cpu = re.findall(r'[0-9]%@[0-9]*', line)
        emc = re.findall(r'EMC_FREQ ([0-9]*)%', line)[0]
        gr3d = re.findall(r'GR3D_FREQ ([0-9]*)%', line)[0]
        pll = re.findall(r'PLL@([0-9]*[.]{0,1}[0-9]*)C', line)[0]
        mcpu = re.findall(r'MCPU@([0-9]*[.]{0,1}[0-9]*)C', line)[0]
        pmic = re.findall(r'PMIC@([0-9]*[.]{0,1}[0-9]*)C', line)[0]
        tboard = re.findall(r'Tboard@([0-9]*[.]{0,1}[0-9]*)C', line)[0]
        gpu = re.findall(r'GPU@([0-9]*[.]{0,1}[0-9]*)C', line)[0]
        bcpu = re.findall(r'BCPU@([0-9]*[.]{0,1}[0-9]*)C', line)[0]
        thermal = re.findall(r'thermal@([0-9]*[.]{0,1}[0-9]*)C', line)[0]
        tdiode = re.findall(r'Tdiode@([0-9]*[.]{0,1}[0-9]*)C', line)[0]
        sys_gpu = re.findall(r'VDD_SYS_GPU ([0-9]*)\/([0-9]*)', line)[0]
        sys_soc = re.findall(r'VDD_SYS_SOC ([0-9]*)\/([0-9]*)', line)[0]
        v0_wifi = re.findall(r'VDD_4V0_WIFI ([0-9]*)\/([0-9]*)', line)[0]
        vdd_in = re.findall(r'VDD_IN ([0-9]*)\/([0-9]*)', line)[0]
        sys_cpu = re.findall(r'VDD_SYS_CPU ([0-9]*)\/([0-9]*)', line)[0]
        sys_ddr = re.findall(r'VDD_SYS_DDR ([0-9]*)\/([0-9]*)', line)[0]

        return [ram, swap, cpu, emc, gr3d, pll, mcpu, pmic, tboard, gpu, bcpu, thermal, tdiode, sys_gpu, sys_soc, v0_wifi, vdd_in, sys_cpu, sys_ddr]

    def parse_file(self, log_file):
        if not os.path.exists(log_file):
            print("Path to file is invalid")
            return

        csv_file = os.path.splitext(log_file)[0] + '.csv'

        with open(csv_file, "w", newline='') as fopen:
            writer = csv.writer(fopen)
            writer.writerow(self.header)

            with open(log_file, 'r') as log:
                data = log.readlines()
                for i, line in enumerate(data):
                    row = self.parse_data(i, line)
                    writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_file', '-i', help='input log file')
    options = parser.parse_args()

    tegrastat = Tegrastat()
    tegrastat.parse_file(options.log_file)
