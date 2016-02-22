#!/usr/bin/env python
# Manage various desktop notifications of periodic tasks

from selenium import webdriver
import sys
import time
import subprocess

# Parse system arguments
opt = ''
val = ''
if len(sys.argv) > 1:
    opt = sys.argv[1]
    if len(sys.argv) > 2:
        val = sys.argv[2]

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


# Choose the right messages depending on opt and val
# No opt, that's very bad
if not opt:
    summary = 'Error!'
    body = 'You called 2do with no arguments. Stop it.'
    icon = iconpath + 'red.gif'

# Time for daily tasks, called by systemd/user/2do.timer
elif opt == '--daily':
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
    if not val:
        body = 'Battery is probably low, connect charger.'
    icon = iconpath + 'red.gif'

else:
    summary = 'Unrecognized!'
    body = 'You called 2do with an unrecognized argument.'
    icon = iconpath + 'red.gif'

# Send the message
subprocess.call(['dbus-send', '--session', '--dest='+dest, path, method,
                 'string:'+app_name, 'uint32:'+pid, 'string:'+icon,
                 'string:'+summary, 'string:'+body, 'array:string:'+actions,
                 'array:string:'+hints, 'int32:'+timeout])


# Do additional things depending on opt and val 
# Open StackExchange sites every day
if opt == '--daily' or opt == '--stack':
    urls = ["http://stackoverflow.com/questions/11227809/",
            "http://math.stackexchange.com/questions/71874/",
            "http://physics.stackexchange.com/questions/5265/",
            "http://music.stackexchange.com/questions/3/",
            "http://superuser.com/questions/792607/",
            "http://tex.stackexchange.com/questions/94889/",
            "http://unix.stackexchange.com/questions/34196/",
            "http://vi.stackexchange.com/questions/84/"]

    # Allow time to kill process with killall python
    if opt == '--daily':
        time.sleep(300)

    # Get Gmail password from password file
    driver = webdriver.Chrome('/usr/bin/chromedriver')
    with open('/home/eyqs/.password', 'r') as f:
        for line in f.readlines():
            if line.split('; ')[0] == 'Gmail':
                user = line.split('; ')[1] + '\n'   # Has newline so no need
                pswd = line.split('; ')[2]          # to click sign in button

    # Sign into StackExchange by logging into Gmail
    driver.get(urls[0])
    driver.find_element_by_xpath(
        "//span[@class='topbar-menu-links']/a[2]").click()
    driver.find_element_by_xpath("//div[@data-provider='google']").click()
    username = driver.find_element_by_name('Email')
    username.send_keys(user)
    driver.implicitly_wait(10)  # Wait for password box to show up
    password = driver.find_element_by_name('Passwd')
    password.send_keys(pswd)

    # Open up all StackExchange sites to get Fanatic badge
    time.sleep(10)      # Wait for server to catch up to logins or something
    for url in urls:
        driver.get(url)
    driver.close()
