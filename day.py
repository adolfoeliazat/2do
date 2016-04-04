#!/usr/bin/env python
# Manage various desktop notifications of periodic tasks
# Split up in order to be able to kill python ../day.py individually
import sys
import time
TIMEFILE = '.2do.log'
if __name__ == '__main__':
    stoptime = int(sys.argv[1])
    currtime = time.time()
    calltime = currtime - currtime % 86400
    try:            # Make sure that TIMEFILE exists
        f = open(TIMEFILE, 'r')
        f.close()
    except:
        f = open(TIMEFILE, 'w')
        f.close()
    flag = 0        # Print '0' if it's time to call
    with open(TIMEFILE, 'r') as f:
        for line in f:
            if float(line.strip()) > calltime:
                flag = 1
    print(flag)
    sys.stdout.flush()
    if flag == 0:   # Wait before calling and writing
        time.sleep(stoptime)
        with open(TIMEFILE, 'a') as f:
            f.write(str(currtime) + '\n')
