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
import sys
import subprocess
if __name__ == '__main__':
    sensors = subprocess.Popen(['sensors'],
        stdout=subprocess.PIPE).communicate()[0].decode('UTF-8').split('\n')
    status = next(x.split() for x in sensors if x.startswith('Physical id 0'))
    # ['Physical', 'id', '0:', '+61.0°C', '(high', '=', '+84.0°C,']
    if float(status[3][:-2]) > float(sys.argv[1]):
        print(0)
    else:
        print(1)
    sys.stdout.flush()
