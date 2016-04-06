# 2do

2do is a simple program that schedules tasks and creates notifications.

## Basics

### Requirements

- D-Bus (already installed if you use systemd)
- GTK+ 3.0
- Python 3.5 with PyGObject 3.10

Probably works on earlier versions too. Definitely does not work on Python 2.

### Installation

    $ git clone https://github.com/eyqs/2do.git/
    $ cd 2do/
    $ vim 2do.py
    $ vim .2do.dat
    $ python 2do.py

## Usage

First, edit `2do.py` and change `TODOPATH` to the location you installed 2do.
Then, edit the sample `.2do.dat` to create the tasks that you want to do.
2do will try its best to do the tasks when you want them to be done, and
notify you following the Desktop Notifications Specification, which usually
means that a small notification will appear at the top right of your screen.

### Configuration

`$2DOPATH` will be literally replaced by whatever you set `TODOPATH` to be.
So, any path can be either an absolute path or a path relative to `$2DOPATH`.
Commands that must be executed in a shell (for example, because they use
a wildcard character `*`) must have `shell=True` as their final argument.
The name is required for every task, but all other parameters are optional:

- name: the name of the task, required but currently does nothing at all;
- summary: the summary of the notification, usually displayed in boldface;
- body: the body of the notification, usually a text block under the summary;
- icon: the path of the icon to display on the notification;
- timeout: the time in milliseconds after which the notification automatically
closes; if the timeout is blank or 0, then the notification never expires;
- execute: the actual command to run when the time has come to do the task;
if there is something in callistrue, then that command must be run first;
- interval: the time in seconds between executions of the task;
- priority: the priority of the task relative to other tasks; lower numbers
correspond to higher priorities, although this really shouldn't matter;
- stoptime: the time in seconds between the notification being displayed
and the task actually executing; useful if the notification is a warning;
- calliftrue: the command to run when the time has come to do the task;
the actual command in execute only runs, and a notification is only created,
if this command runs a program which prints `0` to standard output;
- callonstart: if `Yes`, the task is done immediately after 2do loads;
if `Wait`, the task is done 30 seconds after 2do loads; otherwise, the task
is run after 2do loads based on the time specified in interval.

## License

Copyright © 2016 Eugene Y. Q. Shen.

2do is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version
3 of the License, or (at your option) any later version.

2do is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License in [LICENSE.md][] for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

[license.md]:                ../master/LICENSE.md
                               "The GNU General Public License"
