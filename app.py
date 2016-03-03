#!/usr/bin/env python
# Manage various desktop notifications of periodic tasks
# Split in order to run gtk.main() and scheduler.run() simultaneously

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
