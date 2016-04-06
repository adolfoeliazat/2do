#!/usr/bin/env python
"""
2do v1.0.0
Copyright © 2016 Eugene Y. Q. Shen.

2do is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version
3 of the License, or (at your option) any later version.

2do is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see http://www.gnu.org/licenses/.
"""
import signal
import sys
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as indicator

def quit(item):
    gtk.main_quit()
    os.kill(pid, signal.SIGKILL)
    sys.exit()

def make_menus():
    items = [('Quit', quit)]
    menu = gtk.Menu()
    for item, action in items:
        menuItem = gtk.MenuItem(item)
        menuItem.connect('activate', action)
        menu.append(menuItem)
    menu.append(menuItem)
    menu.show_all()
    return menu

if __name__ == '__main__':
    pid = int(sys.argv[1])
    ap = indicator.Indicator.new('2do_indicator',
                                 '/home/eyqs/Dropbox/Projects/2do/orange.gif',
                                 indicator.IndicatorCategory.SYSTEM_SERVICES)
    ap.set_status(indicator.IndicatorStatus.ACTIVE)
    ap.set_menu(make_menus())
    gtk.main()
