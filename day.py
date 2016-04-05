#!/usr/bin/env python
# Manage various desktop notifications of periodic tasks
# Split up in order to be able to kill python ../day.py individually
import sys
import time
if __name__ == '__main__':
    timefile = sys.argv[1]      # Name of the file to store times
    taskname = sys.argv[2]      # Name of the task to be executed
    modutime = int(sys.argv[3]) # Period of calls; 86400 is daily
    stoptime = int(sys.argv[4]) # Amount of time for user to stop
    currtime = time.time()
    calltime = currtime - currtime % modutime

    # Make sure that timefile exists
    try:
        f = open(timefile, 'r')
        f.close()
    except:
        f = open(timefile, 'w')
        f.close()

    # Read timefile and find taskname
    flag = -1
    contents = []
    with open(timefile, 'r') as f:
        for line in f:
            if line.split(':')[0] == taskname:
                flag = 0
                if float(line.split(':')[1]) > calltime:
                    flag = 1
                    contents.append(taskname + ':' + str(currtime + stoptime))
            else:
                contents.append(line)

    # Add taskname if not found in timefile
    if flag == -1:
        contents.append(taskname + ':' + str(currtime + stoptime))
        flag = 0

    # Wait before calling and writing over timefile
    print(flag)
    sys.stdout.flush()
    if flag == 0:
        time.sleep(stoptime)
        with open(timefile, 'w') as f:
            f.write('\n'.join(contents))
