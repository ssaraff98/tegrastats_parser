###### Tegrastat log file parser ######
import argparse
import csv
import os
import re
import subprocess

header = ["Time Stamp (s)",
          "RAM Used (MB)", "Maximum RAM Available (MB)",
          "SWAP Used (MB)", "Maximum Swap Available (MB)",
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
        self.ram_max = 0
        self.swap_max = 0

    def parse_data(self, i, line):
        ram_used, self.ram_max = re.findall(r'RAM ([0-9]*)\/([0-9]*)MB', line)[0]
        swap_used, self.swap_max = re.findall(r'SWAP ([0-9]*)\/([0-9]*)MB', line)[0]
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
        sys_gpu, avg_sys_gpu = re.findall(r'VDD_SYS_GPU ([0-9]*)\/([0-9]*)', line)[0]
        sys_soc, avg_sys_soc = re.findall(r'VDD_SYS_SOC ([0-9]*)\/([0-9]*)', line)[0]
        v0_wifi, avg_v0_wifi = re.findall(r'VDD_4V0_WIFI ([0-9]*)\/([0-9]*)', line)[0]
        vdd_in, avg_vdd_in = re.findall(r'VDD_IN ([0-9]*)\/([0-9]*)', line)[0]
        sys_cpu, avg_sys_cpu = re.findall(r'VDD_SYS_CPU ([0-9]*)\/([0-9]*)', line)[0]
        sys_ddr, avg_sys_ddr = re.findall(r'VDD_SYS_DDR ([0-9]*)\/([0-9]*)', line)[0]

        return [ram_used, self.ram_max, swap_used, self.swap_max, cpu, emc, gr3d, pll, mcpu, pmic, tboard, gpu, bcpu, thermal, tdiode,
                sys_gpu, avg_sys_gpu, sys_soc, avg_sys_soc, v0_wifi, avg_v0_wifi, vdd_in, avg_vdd_in, sys_cpu, avg_sys_cpu, sys_ddr, avg_sys_ddr]

    def parse_file(self):
        if not os.path.exists(self.log_file):
            print("Path to file is invalid")
            return

        csv_file = os.path.splitext(self.log_file)[0] + '.csv'

        with open(csv_file, "w", newline='') as fopen:
            writer = csv.writer(fopen)

            with open(self.log_file, 'r') as log:
                data = log.readlines()
                writer.writerow(data[0])
                writer.writerow(header)
                hours, minutes, seconds = re.findall(r'([0-9]{2}):([0-9]{2}):([0-9]{2})', data[0])[0]
                time = 0

                for i, line in enumerate(data[1:]):
                    row = [time] + self.parse_data(i, line)
                    writer.writerow(row)
                    time = time + int(self.interval)

if __name__ == '__main__':
    # Command line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--interval', '-i', help='Logging interval in milliseconds for Tegrastats')
    parser.add_argument('--log_file', '-f', help='Log file name for Tegrastats data')
    options = parser.parse_args()

    # Execute tegrastats command
    cmd = f"{{ echo $(date -u) & tegrastats --interval {options.interval}; }} > {options.log_file}"
    process = subprocess.Popen(cmd, shell=True)
    print("Running Tegrastats...\nType and enter 'exit' to stop Tegrastats and parse data.")

    while (True):
        user_input = input()
        if (user_input == "exit"):
                process.kill()
                break

    # Parse tegrastats log file
    tegrastat = Tegrastat(options.interval, options.log_file)
    tegrastat.parse_file()
