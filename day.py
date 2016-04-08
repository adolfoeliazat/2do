#!/usr/bin/env python
"""
2do v1.0.1
Copyright © 2016 Eugene Y. Q. Shen.

2do is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version
3 of the License, or (at your option) any later version.

2do is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see http://www.gnu.org/licenses/.
"""
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
                if float(line.split(':')[1]) < calltime:
                    contents.append(taskname + ':' + str(currtime + stoptime))
                else:
                    flag = 1
                    contents.append(line.strip())
            else:
                contents.append(line.strip())

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
