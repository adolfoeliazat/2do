#!/usr/bin/env python
# Manage various desktop notifications of periodic tasks

import time
import sched
import datetime
import subprocess
DATAFILE = '.2do.dat'
OPENTIME = 30   # Time to wait for X Server to open
STOPTIME = 300  # Time to wait for user to stop 2do
BSUSPEND = True # Suspend when battery less than 5%

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

# Tasks to do: (period in seconds, priority, task name, call on startup)
tasks = [(14400, 1, 'daily', True), (60, 2, 'lowbattery', True),
         (1800, 3, 'break', False), (600, 4, 'fehbg', True)]
scheduler = sched.scheduler()


# Schedule a periodic task
def schedule(interval, priority, task):
    scheduler.enter(interval, priority,
                    lambda i=interval, p=priority, a=task: schedule(i,p,a))
    call(task)
    notify(task)


# Do a task
def call(task):
    if task == 'daily':     # Only run it if not already run today
        today = str(datetime.date.today())
        with open(DATAFILE, 'r+') as f:
            for line in f:
                if today in line:
                    break
            else:           # Wait for STOPTIME, then mark today as run
                scheduler.enter(STOPTIME, 1, lambda a=['python',
                                '/home/eyqs/Dropbox/Projects/2do/web.py']:
                                subprocess.Popen(a))
                scheduler.enter(STOPTIME, 1, lambda t=today, f=f:
                                f.write(t + '\n'))
    elif task == 'fehbg':   # Must use shell to have asterisk wildcard
        subprocess.Popen('feh --bg-fill --randomize --no-fehbg /home/eyqs/' +
            '.config/awesome/2016solarized/wallpapers/*', shell=True)


# Display the right notifications
def notify(task):
    if task == 'daily':
        summary = 'Keep that StackExchange streak!'
        body = 'Automatically opening all tabs in ' + str(STOPTIME) + \
               ' seconds.\nTerminate with `killall python`.'
        icon = iconpath + 'yellow.gif'
    elif task == 'break':
        summary = 'Take a break!'
        body = 'Rest your eyes for 5 minutes.'
        icon = iconpath + 'orange.gif'
    elif task == 'fehbg':
        summary = 'New wallpaper!'
        body = "You don't need a notification to notice it..."
        icon = iconpath + 'magenta.gif'
    elif task == 'lowbattery':
        global BSUSPEND
        status = subprocess.Popen(['acpi'],
            stdout=subprocess.PIPE).communicate()[0].decode('UTF-8').split()
        # ['Battery', '0:', 'Discharging,', '13%,']
        if status[2] != 'Discharging,':
            return
        amount = int(status[3][:-2])
        if amount > 20:
            return
        if amount < 5 and BSUSPEND:
            subprocess.call(['systemctl', 'suspend'])
            BSUSPEND = False
        summary = 'Low battery!'
        body = 'Battery at ' + str(amount) + '%, connect charger.'
        icon = iconpath + 'red.gif'
    else:
        summary = 'Unrecognized!'
        body = 'You called 2do with an unrecognized argument.'
        icon = iconpath + 'red.gif'

    subprocess.call(['dbus-send', '--session', '--dest=' + dest, path, method,
                     'string:' + app_name, 'uint32:' + pid, 'string:' + icon,
                     'string:'+summary,'string:'+body,'array:string:'+actions,
                     'array:string:' + hints, 'int32:' + timeout])


if __name__ == '__main__':
    # Make sure that DATAFILE exists
    try:
        f = open(DATAFILE, 'r')
        f.close()
    except:
        f = open(DATAFILE, 'w')
        f.close()

    # Call some tasks immediately
    for task in tasks:
        if task[3]:
            call(task[2])
            notify(task[2])

    # Schedule all tasks periodically
    for task in tasks:
        scheduler.enter(task[0], task[1], lambda
                        i=task[0], p=task[1], a=task[2]: schedule(i,p,a))
    scheduler.run()
