#!/usr/bin/env bash
# Open up test desktop notification
# Based on http://cheesehead-techblog.blogspot.ca/2012/07/dbus-tutorial-intro-and-resources.html

dest="org.freedesktop.Notifications"
path="/org/freedesktop/Notifications"
method="org.freedesktop.Notifications.Notify"

# Only middle line is actual message data
# Message data sandwiched by stuff needed for naughty
dbus-send --session --dest="$dest" "$path" "$method" \
          string:"" uint32:0 string:"" \
          string:"test" string:"hello world" \
          array:string:"" array:string:"" int32:-1
