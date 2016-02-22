#!/usr/bin/env python
# Manage various desktop notifications of periodic tasks

from selenium import webdriver
import time
import sched
import subprocess
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

# Tasks to do: (period in seconds, priority, task name)
tasks = [(86400, 1, 'daily'), (60, 2, 'lowbattery'),
         (1800, 3, 'break'), (600, 4, 'fehbg')]
scheduler = sched.scheduler()


# Do a periodic task
def call(interval, priority, task):
    global BSUSPEND
    # Reschedule the task
    scheduler.enter(interval, priority,
                    lambda i=interval, p=priority, a=task: call(i,p,a))

    # Choose the right messages depending on task
    # Time for daily tasks
    if task == 'daily':
        summary = 'Keep that StackExchange streak!'
        body = 'Automatically opening all tabs in ' + str(STOPTIME) + \
               ' seconds.\nTerminate with `killall python`.'
        icon = iconpath + 'yellow.gif'
    # Time to take a break
    elif task == 'break':
        summary = 'Take a break!'
        body = 'Rest your eyes for 5 minutes.'
        icon = iconpath + 'orange.gif'
    # Time to switch wallpapers
    elif task == 'fehbg':
        summary = 'New wallpaper!'
        body = "You don't need a notification to notice it..."
        icon = iconpath + 'magenta.gif'
    # Time to check the battery level
    elif task == 'lowbattery':
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

    # Send the message
    subprocess.call(['dbus-send', '--session', '--dest=' + dest, path, method,
                     'string:' + app_name, 'uint32:' + pid, 'string:' + icon,
                     'string:'+summary,'string:'+body,'array:string:'+actions,
                     'array:string:' + hints, 'int32:' + timeout])

    # Do extra stuff
    if task == 'daily':
        scheduler.enter(OPENTIME, 1, lambda a=['python',
            '/home/eyqs/Dropbox/Projects/2do/web.py']: subprocess.Popen(a))
    elif task == 'fehbg':   # Must use shell to have asterisk wildcard
        subprocess.Popen('feh --bg-fill --randomize --no-fehbg /home/eyqs/' +
            '.config/awesome/2016solarized/wallpapers/*', shell=True)


if __name__ == '__main__':
#    time.sleep(OPENTIME)
    for task in tasks:
        scheduler.enter(task[0], task[1],
                        lambda i=task[0], p=task[1], a=task[2]: call(i,p,a))
    scheduler.run()
