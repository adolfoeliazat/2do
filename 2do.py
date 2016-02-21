#!/usr/bin/env python
# Manage various desktop notifications of periodic tasks

import sys
import time
import subprocess

if len(sys.argv) > 1:
    opt = sys.argv[1]
    if len(sys.argv) > 2:
        val = sys.argv[2]

dest = 'org.freedesktop.Notifications'
path = '/org/freedesktop/Notifications'
method = 'org.freedesktop.Notifications.Notify'
iconpath = '/home/eyqs/Dropbox/Projects/2do/'
app_name = '2do'
pid = ''
actions = ''
hints = ''
timeout = '0'       # No timeout, everything manually dismissed


# Time for daily tasks, called by systemd/user/2do.timer
if opt == '--daily':
    time.sleep(30)  # Allow time for X server to open
    summary = 'Keep that StackExchange streak!'
    body = 'Automatically opening all tabs in 300 seconds.\n' + \
           'Terminate with `killall python`.'
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
    icon = iconpath + 'red.gif'


subprocess.call(['dbus-send', '--session', '--dest='+dest, path, method,
                 'string:'+app_name, 'uint32:'+pid, 'string:'+icon,
                 'string:'+summary, 'string:'+body, 'array:string:'+actions,
                 'array:string:'+hints, 'int32:'+timeout])

if opt == '--daily':
    subprocess.call(['python', '/home/eyqs/Dropbox/Projects/2do/web.py','-s'])
