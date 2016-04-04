#!/usr/bin/env python
# Manage various desktop notifications of periodic tasks

import os
import time
import sched
import subprocess
DATAFILE = '.2do.dat'
DLOGFILE = '.2do.log'
OPENTIME = 30   # Time to wait for X Server to open
STOPTIME = 300  # Time to wait for user to stop 2do

# Keep dbus-send constants
dest = 'org.freedesktop.Notifications'
path = '/org/freedesktop/Notifications'
method = 'org.freedesktop.Notifications.Notify'
iconpath = '/home/eyqs/Dropbox/Projects/2do/'
app_name = '2do'
pid = ''
actions = ''
hints = ''
timeout = '0'       # No timeout, everything manually dismissed


# Parse DATAFILE to find the tasks to do
def parse():
    tasklist = []
    with open(DATAFILE) as f:
        curr = {'summary':'', 'body':'', 'icon':'',
                'execute':'', 'interval':'', 'priority':'',
                'calliftrue':'', 'callonstart':''}
        for line in f:
            if line.startswith('#'):
                continue
            if not line.strip():
                tasklist.append(curr)
                curr = {'summary':'', 'body':'', 'icon':'',
                        'execute':'', 'interval':'', 'priority':'',
                        'calliftrue':'', 'callonstart':''}
            else:
                split = line.split(':')
                if len(split) > 1:
                    curr[split[0]] = split[1].strip()
        tasklist.append(curr)
    return tasklist


# Schedule a periodic task
def schedule(interval, priority, execute, calliftrue):
    scheduler.enter(interval, priority, lambda
        i=interval, p=priority, e=execute, c=calliftrue: schedule(i,p,e,c))

    # Call the task
    if task['execute']:
        exe = task['execute'].split(',')
        if exe[-1] == 'shell=True':
            subprocess.Popen(' '.join(exe[:-1]), shell=True)
        else:
            subprocess.Popen(exe)

    # Display the right notifications
    summary = task['summary']
    body = task['body']
    icon = iconpath + task['icon']
    subprocess.call(['dbus-send', '--session', '--dest=' + dest, path, method,
                     'string:' + app_name, 'uint32:' + pid, 'string:' + icon,
                     'string:'+summary,'string:'+body,'array:string:'+actions,
                     'array:string:' + hints, 'int32:' + timeout])


if __name__ == '__main__':
    # Parse the tasklist, start the scheduler, create the appindicator
    tasklist = parse()
    scheduler = sched.scheduler()
    subprocess.Popen(['python', '/home/eyqs/Dropbox/Projects/2do/app.py',
                      str(os.getpid())])

    # Make sure that DLOGFILE exists
    try:
        f = open(DLOGFILE, 'r')
        f.close()
    except:
        f = open(DLOGFILE, 'w')
        f.close()

    # Call some tasks immediately and others periodically
    for task in tasklist:
        if task['callonstart'] == 'Yes':
            delay = 0
        elif task['callonstart'] == 'Wait':
            delay = OPENTIME
        else:
            delay = int(task['interval'])
        scheduler.enter(delay, int(task['priority']),
            lambda i=int(task['interval']), p=int(task['priority']),
                   e=task['execute'], c=task['calliftrue']: schedule(i,p,e,c))
    scheduler.run()
