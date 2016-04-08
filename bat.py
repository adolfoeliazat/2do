#!/usr/bin/env python
"""
2do v1.0.1
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
import sys
import subprocess
if __name__ == '__main__':
    status = subprocess.Popen(['acpi'],
        stdout=subprocess.PIPE).communicate()[0].decode('UTF-8').split()
    # ['Battery', '0:', 'Discharging,', '13%,']
    if status[2] == 'Discharging,' and float(status[3][:-2]) < float(sys.argv[1]):
        print(0)
        if float(status[3][:-2]) < float(sys.argv[2]):
            subprocess.call(['systemctl', 'suspend'])
    else:
        print(1)
    sys.stdout.flush()
