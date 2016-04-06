#!/usr/bin/env python
# Return '0' if temperature is high
import sys
import subprocess
if __name__ == '__main__':
    sensors = subprocess.Popen(['sensors'],
        stdout=subprocess.PIPE).communicate()[0].decode('UTF-8').split('\n')
    status = next(x.split() for x in sensors if x.startswith('Physical id 0'))
    # ['Physical', 'id', '0:', '+61.0°C', '(high', '=', '+84.0°C,']
    if float(status[3][:-2]) > float(sys.argv[1]):
        print(0)
    else:
        print(1)
    sys.stdout.flush()
