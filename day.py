#!/usr/bin/env python
# Manage various desktop notifications of periodic tasks
# Split up in order to be able to kill python ../day.py individually

import sys
import time
import datetime

if __name__ == '__main__':
    datafile = sys.argv[1]
    stoptime = int(sys.argv[2])
    today = str(datetime.date.today())

    flag = 0    # Print '0' to make 2do call and notify
    with open(datafile, 'r') as f:
        for line in f:
            if today in line:
                flag = 1
    print(flag)
    sys.stdout.flush()

    if flag == 0:   # Only write to file after 2do calls
        time.sleep(stoptime)
        with open(datafile, 'a') as f:
            f.write(today + '\n')
