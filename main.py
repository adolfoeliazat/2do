#!/usr/bin/env python
# Manage different instances of 2do

import sched
import subprocess

def call(interval, priority, *arguments):
    subprocess.call(['python', '/home/eyqs/Dropbox/Projects/2do/2do.py']
                    + list(arguments))
    scheduler.enter(interval, priority, lambda i=interval, p=priority,
                    a=arguments: call(i,p,*a))

scheduler = sched.scheduler()
tasks = [(30, 1, '--daily'), (10, 1, '--break'),
         (9, 1, '--lowbattery', '3')]
for task in tasks:
    scheduler.enter(task[0], task[1], lambda i=task[0], p=task[1],
                    a=task[2:]: call(i,p,*a))
scheduler.run()
