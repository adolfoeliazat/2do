#!/usr/bin/env python
# Return '0' if battery below 15%
import subprocess
if __name__ == '__main__':
    status = subprocess.Popen(['acpi'],
        stdout=subprocess.PIPE).communicate()[0].decode('UTF-8').split()
    # ['Battery', '0:', 'Discharging,', '13%,']
    if status[2] != 'Discharging,':
        print(1)
    if int(status[3][:-2]) > 15:
        print(1)
    else:
        print(0)
    sys.stdout.flush()
