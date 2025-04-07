#!/usr/bin/env python3

# convert list from MIB to dict

import sys
import re

pattern = re.compile("\s+(.+)\s+\((\d+)\),?")

for line in sys.stdin.readlines():
    m = pattern.search(line)
    if m:
        print('"' + m.group(2) + '": "' + m.group(1) + '",')
