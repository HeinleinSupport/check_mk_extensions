#!/usr/bin/env python3

#
# (C) 2023 Heinlein Support GmbH - License: GNU General Public License v2
# Robert Sander <r.sander@heinlein-support.de>
#

import sys
import argparse
import checkmkapi
from pprint import pprint

oncall = 'oncall'
workhours = 'workhours'
workdays = [{'day': 'monday',    'time_ranges': [{'start': '09:00', 'end': '18:00'}]},
            {'day': 'tuesday',   'time_ranges': [{'start': '09:00', 'end': '18:00'}]},
            {'day': 'wednesday', 'time_ranges': [{'start': '09:00', 'end': '18:00'}]},
            {'day': 'thursday',  'time_ranges': [{'start': '09:00', 'end': '18:00'}]},
            {'day': 'friday',    'time_ranges': [{'start': '09:00', 'end': '15:00'}]},
            ]
always =   [{'day': 'monday',    'time_ranges': [{'start': '00:00', 'end': '24:00'}]},
            {'day': 'tuesday',   'time_ranges': [{'start': '00:00', 'end': '24:00'}]},
            {'day': 'wednesday', 'time_ranges': [{'start': '00:00', 'end': '24:00'}]},
            {'day': 'thursday',  'time_ranges': [{'start': '00:00', 'end': '24:00'}]},
            {'day': 'friday',    'time_ranges': [{'start': '00:00', 'end': '24:00'}]},
            {'day': 'saturday',  'time_ranges': [{'start': '00:00', 'end': '24:00'}]},
            {'day': 'sunday',    'time_ranges': [{'start': '00:00', 'end': '24:00'}]},
            ]

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url', help='URL to Check_MK site')
parser.add_argument('-u', '--username', help='name of the automation user')
parser.add_argument('-p', '--password', help='secret of the automation user')
parser.add_argument('-r', '--region', required=True, help='region')
parser.add_argument('-k', '--shortcut', required=True, help='region shortcut')
parser.add_argument('-D', '--debug', action='store_true', required=False)

args = parser.parse_args()
if args.debug:
    pprint(args)

cmk = checkmkapi.CMKRESTAPI(args.url, args.username, args.password)

#
# Timeperiods
#

cmk.create_timeperiod('%s_%s' % (workhours, args.shortcut),
                      '%s %s' % (workhours.capitalize(), args.region),
                      workdays)
cmk.create_timeperiod('%s_%s' % (oncall, args.shortcut),
                      '%s %s' % (oncall.capitalize(), args.region),
                      always,
                      exclude=['%s_%s' % (workhours, args.shortcut)])


#
# Activate Changes
#

cmk.activate()
