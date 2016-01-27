#!/usr/bin/env bash
# Open up test desktop notification
# Based on http://cheesehead-techblog.blogspot.ca/2012/07/dbus-tutorial-intro-and-resources.html

dest="org.freedesktop.Notifications"
path="/org/freedesktop/Notifications"
method="org.freedesktop.Notifications.Notify"

app_name=""
id=0
icon=""
summary="test"
body="hello world"
actions=""
hints=""
timeout=5000    # Stay for 5 seconds

# Get list of arguments for any destination
dbus-send --print-reply --dest="$dest" "$path" \
          org.freedesktop.DBus.Introspectable.Introspect

# Open up test desktop notification
dbus-send --session --dest="$dest" "$path" "$method" \
          string:"$app_name" uint32:$id string:"$icon" \
          string:"$summary" string:"$body" \
          array:string:"$actions" array:string:"$hints" int32:$timeout
