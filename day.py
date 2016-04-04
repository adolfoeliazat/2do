#!/usr/bin/env python
# Manage various desktop notifications of periodic tasks
# Split up in order to be able to kill python ../day.py individually
import sys
import time
if __name__ == '__main__':
    timefile = sys.argv[1]      # Name of the file to store times
    modutime = int(sys.argv[2]) # Period of calls; 86400 is daily
    stoptime = int(sys.argv[3]) # Amount of time for user to stop
    currtime = time.time()
    calltime = currtime - currtime % modutime

    # Make sure that timefile exists
    try:
        f = open(timefile, 'r')
        f.close()
    except:
        f = open(timefile, 'w')
        f.close()

    # Print '0' if it's time to call
    flag = 0
    with open(timefile, 'r') as f:
        for line in f:
            if float(line.strip()) > calltime:
                flag = 1
    print(flag)
    sys.stdout.flush()

    # Wait before calling and writing
    if flag == 0:
        time.sleep(stoptime)
        with open(timefile, 'a') as f:
            f.write(str(currtime) + '\n')
