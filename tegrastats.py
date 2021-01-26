import subprocess

class Tegrastats:
    def __init__(self, interval, log_file, verbose):
        self.interval = interval
        self.log_file = log_file
        self.verbose = verbose

    def prepare_command(self):
        tegrastats_cmd = f"tegrastats --interval {self.interval}"

        if self.verbose:
            tegrastats_cmd = tegrastats_cmd + " --verbose"

        cmd = f"{{ echo $(date -u) & {tegrastats_cmd}; }} > {self.log_file}"
        return cmd

    def run(self):
        cmd = self.prepare_command()
        process = None

        try:
            process = subprocess.Popen(cmd, shell=True)
            print("Running tegrastats...\nEnter 'exit' to stop tegrastats and parse data\n")
        except subprocess.CalledProcessError:
            print(f"Error running tegrastats!\nCommand used {cmd}")
            return False

        while (True):
            user_input = input()
            if (user_input == "exit"):
                try:
                    process.kill()
                    print("Successfully stopped tegrastats!")
                    break
                except subprocess.CalledProcessError:
                    print(f"Unable to kill tegrastats (pid={process.pid}) successfully...")
                    return False

        return True

if __name__ == '__main__':
    interval = 1000
    log_file = 'output_log.txt'
    verbose = False

    tegrastats = Tegrastats(interval, log_file, verbose)
    tegrastats.run()
