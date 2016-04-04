#!/usr/bin/env python
# Return '0' if battery is low
import sys
import subprocess
if __name__ == '__main__':
    status = subprocess.Popen(['acpi'],
        stdout=subprocess.PIPE).communicate()[0].decode('UTF-8').split()
    # ['Battery', '0:', 'Discharging,', '13%,']
    if status[2] == 'Discharging,' and int(status[3][:-2]) < int(sys.argv[1]):
        print(0)
        if int(status[3][:-2]) < int(sys.argv[2]):
            subprocess.call(['systemctl', 'suspend'])
    else:
        print(1)
    sys.stdout.flush()
