###### Tegrastat log file parser ######
import argparse
import csv
import os
import re
import subprocess

# Sample output
# RAM 1404/7860MB (lfb 236x4MB) SWAP 0/3930MB (cached 0MB) CPU [0%@345,0%@960,0%@960,0%@345,0%@345,0%@345]
# EMC_FREQ 0% GR3D_FREQ 0% PLL@35.5C MCPU@35.5C PMIC@100C Tboard@30C GPU@32C BCPU@35.5C thermal@34.1C Tdiode@31.5C
# VDD_SYS_GPU 153/153 VDD_SYS_SOC 306/306 VDD_4V0_WIFI 0/0 VDD_IN 1649/1649 VDD_SYS_CPU 306/306 VDD_SYS_DDR 173/173
header = ["Time Stamp",
          "RAM (MB)",
          "SWAP (MB)",
          "IRAM (KB)",
          "CPU (%) / FREQ (MHz)",
          "EMC FREQ (%)",
          "GR3D FREQ (%)",
          "PLL Temperature (C)",
          "MCPU Temperature (C)",
          "PMIC (C)",
          "Tboard Temperature (C)",
          "GPU Temperature (C)",
          "BCPU Temperature (C)",
          "Thermal Temperature (C)",
          "Tdiode Temperature(C)",
          "Current GPU Power Consumption(mW)", "Average GPU Power Consumption(mW)",
          "Current SOC Power Consumption(mW)", "Average SOC Power Consumption(mW)",
          "Current WIFI Power Consumption(mW)", "Average WIFI Power Consumption(mW)",
          "Current IN Power Consumption(mW)", "Average IN Power Consumption(mW)",
          "Current CPU Power Consumption(mW)", "Average CPU Power Consumption(mW)",
          "Current DDR Power Consumption(mW)", "Average DDR Power Consumption(mW)",]

class Tegrastat:
    def __init__(self, interval, log_file):
        self.interval = interval
        self.log_file = log_file

    def parse_data(self, i, line):
        ram_used, ram_max = re.findall(r'RAM ([0-9]*)\/([0-9]*)MB', line)[0]
        swap_used, swap_max = re.findall(r'SWAP ([0-9]*)\/([0-9]*)MB', line)[0]
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

        return [ram_used, swap_used, cpu, emc, gr3d, pll, mcpu, pmic, tboard, gpu, bcpu, thermal, tdiode, sys_gpu, sys_soc, v0_wifi, vdd_in, sys_cpu, sys_ddr]

    def parse_file(self):
        if not os.path.exists(self.log_file):
            print("Path to file is invalid")
            return

        csv_file = os.path.splitext(self.log_file)[0] + '.csv'

        with open(csv_file, "w", newline='') as fopen:
            writer = csv.writer(fopen)
            # writer.writerow(header)

            with open(self.log_file, 'r') as log:
                data = log.readlines()
                print(data[0])
                # writer.writerow(data[0])
                # hours, minutes, seconds = re.findall(r'([0-9]{2}):([0-9]{2}):([0-9]{2})', data[0])
                # print(data[0])
        #
        #         for i, line in enumerate(data[1:]):
        #             row = self.parse_data(i, line)
        #             writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--interval', '-i', help='Logging interval in milliseconds for Tegrastats')
    parser.add_argument('--log_file', '-f', help='Log file name for Tegrastats data')
    options = parser.parse_args()

    # Execute tegrastats command
    cmd = f"{{ echo $(date -u) & tegrastats --interval {options.interval}; }} > {options.log_file}"
    process = subprocess.Popen(cmd, shell=True)
    print("Running Tegrastats...\nPress CTRL-C to stop and parse data.")

    while (True):
        user_input = input()
        if (user_input == "exit"):
                process.kill()
                break

    tegrastat = Tegrastat(options.interval, options.log_file)
    tegrastat.parse_file()
