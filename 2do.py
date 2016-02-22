#!/usr/bin/env python
# Manage various desktop notifications of periodic tasks

from selenium import webdriver
import time
import sched
import subprocess
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

# Tasks to do: (period in seconds, priority, extra arguments)
tasks = [(16, 1, '--daily'), (17, 2, '--lowbattery', '5'), (14, 3, '--break')]
scheduler = sched.scheduler()


# Do a task
def call(interval, priority, *arguments):
    # Parse extra arguments
    opt = ''
    val = ''
    if len(arguments) > 0:
        opt = arguments[0]
        if len(arguments) > 1:
            val = arguments[1]

    # Choose the right messages depending on opt
    # No opt, that's very bad
    if not opt:
        summary = 'Error!'
        body = 'You called 2do with no arguments. Stop it.'
        icon = iconpath + 'red.gif'
    # Time for daily tasks, called by systemd/user/2do.timer
    elif opt == '--daily':
        summary = 'Keep that StackExchange streak!'
        body = 'Automatically opening all tabs in ' + str(STOPTIME) + \
               ' seconds.\nTerminate with `killall python`.'
        icon = iconpath + 'yellow.gif'
    # Time to take a break, called by systemd/user/30min.timer
    elif opt == '--break':
        summary = 'Take a break!'
        body = 'Rest your eyes for 5 minutes.'
        icon = iconpath + 'orange.gif'
    # Laptop battery getting low, called by bin/lowbattery
    elif opt == '--lowbattery':
        summary = 'Low battery!'
        body = 'Battery at ' + val + '%, connect charger.'
        if not val:
            body = 'Battery is probably low, connect charger.'
        icon = iconpath + 'red.gif'
    else:
        summary = 'Unrecognized!'
        body = 'You called 2do with an unrecognized argument.'
        icon = iconpath + 'red.gif'

    # Send the message
    subprocess.call(['dbus-send', '--session', '--dest=' + dest, path, method,
                     'string:' + app_name, 'uint32:' + pid, 'string:' + icon,
                     'string:'+summary,'string:'+body,'array:string:'+actions,
                     'array:string:' + hints, 'int32:' + timeout])

    # Do extra stuff
    if opt == '--daily':
        scheduler.enter(OPENTIME, 1, lambda a=['python',
            'home/eyqs/Dropbox/Projects/2do/web.py']: subprocess.Popen(a))

    # Reschedule the task
    scheduler.enter(interval, priority,
                    lambda i=interval, p=priority, a=arguments: call(i,p,*a))


if __name__ == '__main__':
    time.sleep(OPENTIME)
    for task in tasks:
        scheduler.enter(task[0], task[1],
                        lambda i=task[0], p=task[1], a=task[2:]: call(i,p,*a))
    scheduler.run()
