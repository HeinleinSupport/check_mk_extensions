#!/usr/bin/env python3

import sys
import cmk.utils.paths
import os.path
from pprint import pprint

hostname = sys.argv[1]

with open(os.path.join(cmk.utils.paths.counters_dir, hostname), "r") as counterfile:
    counter = eval(counterfile.read())
    pprint(counter)
