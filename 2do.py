#!/usr/bin/env python
# Manage various desktop notifications of periodic tasks
import os
import time
import sched
import subprocess
TODOPATH = '/home/eyqs/Dropbox/Projects/2do'
DATAFILE = TODOPATH + '/.2do.dat'

# Keep dbus-send constants
dest = 'org.freedesktop.Notifications'
path = '/org/freedesktop/Notifications'
method = 'org.freedesktop.Notifications.Notify'
app_name = '2do'
pid = ''
actions = ''
hints = ''

# Parse DATAFILE to find the tasks to do
def parse():
    tasklist = {}
    with open(DATAFILE) as f:
        for line in f:
            split = line.split(':')
            if split[0].strip() == 'name':
                curr = {'summary':'', 'body':'', 'icon':'','execute':'',
                        'timeout':'', 'interval':'', 'priority':'',
                        'stoptime':'', 'calliftrue':'', 'callonstart':''}
                tasklist[split[1].strip()] = curr
            elif len(split) > 1:
                curr[split[0].strip()] = \
                    split[1].strip().replace('$2DOPATH', TODOPATH)
    return tasklist

# Schedule the tasks to do
def schedule(interval, priority, task):
    scheduler.enter(interval, priority, lambda
                    i=interval, p=priority, t=task: schedule(i,p,t))
    if task['calliftrue']:      # Only call the task if stdout is '0'
        check = subprocess.Popen(task['calliftrue'].split(),
                                 stdout=subprocess.PIPE)
        if check.stdout.readline() != b'0\n':
            return
        if task['stoptime']:    # Wait for stoptime to allow user to stop
            scheduler.enter(int(task['stoptime']), int(task['priority']),
                lambda c=check, t=task: stillalive(c,t))
            notify(task)
            return
    call(task)
    notify(task)

# If user did not kill the checking script, call the task
def stillalive(check, task):
    if not check.poll():
        call(task)

# Do the task to do
def call(task):
    if task['execute']:
        exe = task['execute'].split()
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
    subprocess.Popen(['python', TODOPATH + '/app.py', str(os.getpid())])
    # Call some tasks immediately and others periodically
    for name, task in tasklist.items():
        if task['callonstart'] == 'Yes':
            delay = 0
        elif task['callonstart'] == 'Wait':
            delay = 30
        else:
            delay = int(task['interval'])
        scheduler.enter(delay, int(task['priority']), lambda
                        i=int(task['interval']), p=int(task['priority']),
                        t=task: schedule(i,p,t))
    scheduler.run()
