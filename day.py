#!/usr/bin/env python
# Manage various desktop notifications of periodic tasks
# Split up in order to be able to kill python ../day.py individually

import sys
import time

if __name__ == '__main__':
    datafile = sys.argv[1]          # File has the call times
    stoptime = int(sys.argv[2])     # Time to stop the script
    calltime = float(sys.argv[3])   # Call it after this time

    flag = 0        # Print '0' if it's time to call
    with open(datafile, 'r') as f:
        for line in f:
            if float(line.strip()) > calltime:
                flag = 1
    print(flag)
    sys.stdout.flush()

    if flag == 0:   # Wait before calling and writing
        time.sleep(stoptime)
        with open(datafile, 'a') as f:
            f.write(str(time.time()) + '\n')
