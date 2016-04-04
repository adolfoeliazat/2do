#!/usr/bin/env python
# Manage various desktop notifications of periodic tasks

import os
import time
import sched
import subprocess
DATAFILE = '.2do.dat'

# Keep dbus-send constants
dest = 'org.freedesktop.Notifications'
path = '/org/freedesktop/Notifications'
method = 'org.freedesktop.Notifications.Notify'
iconpath = '/home/eyqs/Dropbox/Projects/2do/'
app_name = '2do'
pid = ''
actions = ''
hints = ''

# Parse DATAFILE to find the tasks to do
def parse():
    tasklist = []
    with open(DATAFILE) as f:
        curr = {'summary':'', 'body':'', 'icon':'','execute':'',
                'timeout':'', 'interval':'', 'priority':'',
                'stoptime':'', 'calliftrue':'', 'callonstart':''}
        for line in f:
            if line.startswith('#'):
                continue
            if not line.strip():
                tasklist.append(curr)
                curr = {'summary':'', 'body':'', 'icon':'','execute':'',
                        'timeout':'', 'interval':'', 'priority':'',
                        'stoptime':'', 'calliftrue':'', 'callonstart':''}
            else:
                split = line.split(':')
                if len(split) > 1:
                    curr[split[0]] = split[1].strip()
        tasklist.append(curr)
    return tasklist

# Schedule the tasks to do
def schedule(interval, priority, task):
    scheduler.enter(interval, priority, lambda
                    i=interval, p=priority, t=task: schedule(i,p,t))
    if task['execute']:             # Call the task
        if task['calliftrue']:      # Only call the task if stdout is '0'
            check = subprocess.Popen(task['calliftrue'].split(','),
                                     stdout=subprocess.PIPE)
            if check.stdout.readline() != b'0\n':
                return
            if task['stoptime']:    # Wait for stoptime to allow user to stop
                scheduler.enter(int(task['stoptime']), 1,
                    lambda c=check, t=task: stillalive(c,t))
                notify(task)
                return
        call(task)
        notify(task)
    else:
        notify(task)

# If user did not kill the checking script, call the task
def stillalive(check, task):
    if not check.poll():
        call(task)

# Do the task to do
def call(task):
    exe = task['execute'].split(',')
    if exe[-1] == 'shell=True':
        subprocess.Popen(' '.join(exe[:-1]), shell=True)
    else:
        subprocess.Popen(exe)

# Notify the task to do
def notify(task):
    summary = task['summary']
    body = task['body']
    icon = task['icon']
    timeout = task['timeout']
    subprocess.call(['dbus-send', '--session', '--dest=' + dest, path, method,
                     'string:' + app_name, 'uint32:' + pid, 'string:' + icon,
                     'string:'+summary,'string:'+body,'array:string:'+actions,
                     'array:string:' + hints, 'int32:' + timeout])

if __name__ == '__main__':
    # Parse the tasklist, start the scheduler, and create the appindicator
    tasklist = parse()
    scheduler = sched.scheduler()
    subprocess.Popen(['python', '/home/eyqs/Dropbox/Projects/2do/app.py',
                      str(os.getpid())])
    # Call some tasks immediately and others periodically
    for task in tasklist:
        if task['callonstart'] == 'Yes':
            delay = 0
        elif task['callonstart'] == 'Wait':
            delay = 10
        else:
            delay = int(task['interval'])
        scheduler.enter(delay, int(task['priority']), lambda
                        i=int(task['interval']), p=int(task['priority']),
                        t=task: schedule(i,p,t))
    scheduler.run()
