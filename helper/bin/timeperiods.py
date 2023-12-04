#!/usr/bin/env python3

#
# (C) 2023 Heinlein Support GmbH - License: GNU General Public License v2
# Robert Sander <r.sander@heinlein-support.de>
#

import sys
import argparse
import checkmkapi
import requests
from datetime import date
from pprint import pprint

apifeiertage = 'https://get.api-feiertage.de/'

laender = {
    'bb': 'Brandenburg',
    'be': 'Berlin',
    'bw': 'Baden-Württemberg',
    'by': 'Bayern',
    'hb': 'Bremen',
    'hh': 'Hamburg',
    'he': 'Hessen',
    'mv': 'Mecklenburg-Vorpommern',
    'ni': 'Niedersachsen',
    'nw': 'Nordrhein-Westfalen',
    'rp': 'Rheinland-Pfalz',
    'sl': 'Saarland',
    'sn': 'Sachsen',
    'st': 'Sachsen-Anhalt',
    'sh': 'Schleswig-Holstein',
    'th': 'Thüringen',
}

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url', help='URL to Check_MK site')
parser.add_argument('-u', '--username', help='name of the automation user')
parser.add_argument('-p', '--password', help='secret of the automation user')
parser.add_argument('-D', '--debug', action='store_true', required=False)
subparsers = parser.add_subparsers(title='available commands', help='call "subcommand --help" for more information')
delete_timeperiod = subparsers.add_parser('delete', help='delete timeperiod')
delete_timeperiod.set_defaults(func='delete_timeperiod')
delete_timeperiod.add_argument('name', help='name of timeperiod')
dump_timeperiods = subparsers.add_parser('dump', help='dump timeperiods')
dump_timeperiods.set_defaults(func='dump_timeperiods')
create_timeperiod = subparsers.add_parser('create', help='create timeperiod from api-feiertage.de')
create_timeperiod.set_defaults(func='create_timeperiod')
create_timeperiod.add_argument('-a', '--all-states', action='store_true', required=False, help='Nur bundesweite Feiertage')
create_timeperiod.add_argument('-s', '--state', choices=laender.keys(), help='Bundesland', required=False)
create_timeperiod.add_argument('-y', '--year', required=False)
create_timeperiod.add_argument('-c', '--current-year', action='store_true', required=False)
create_timeperiod.add_argument('-e', '--exclude-in', required=False, help='Exclude in anderer Timeperiod')

args = parser.parse_args()
if 'func' not in args:
    parser.print_help()
    sys.exit(1)
if args.debug:
    pprint(args)

cmk = checkmkapi.CMKRESTAPI(args.url, args.username, args.password)

if args.func == 'dump_timeperiods':
    pprint(cmk.get_timeperiods()[0])

if args.func == 'delete_timeperiod':
    tp, etag = cmk.get_timeperiod(args.name)
    cmk.delete_timeperiod(args.name, etag)

if args.func == 'create_timeperiod':
    params = {}
    name = 'feiertage_'
    alias = 'Feiertage '
    year = None
    if args.current_year:
        year = str(date.today().year)
    elif args.year:
        year = args.year
    if year:
        params['years'] = year
        name += year
        alias += year
    if args.all_states:
        params['all_states'] = "true"
        name += '_bundeseinheitlich'
        alias += ' bundeseinheitlich'
    elif args.state:
        params['states'] = args.state
        name += '_%s' % args.state
        alias += ' %s' % laender[args.state]

    if args.debug:
        pprint(params)

    if not params:
        print('Please give at least a year or a state.\n')
        create_timeperiod.print_help()
        sys.exit(1)
        
    resp = requests.get(apifeiertage, params=params)
    if resp.content:
        try:
            data = resp.json()
        except json.decoder.JSONDecodeError:
            data = resp.content
    else:
        data = {}
    if resp.status_code >= 400:
        sys.stderr.write("%r\n" % data)
    
    if not data.get('feiertage'):
        print('Error: %s' % data.get('additional_note'))
        sys.exit(1)
    else:
        exceptions = []
        for feiertag in data['feiertage']:
            exceptions.append({'date': feiertag['date'], 'time_ranges': [ { 'start': '00:00:00', 'end': '24:00:00' } ]})

        if args.debug:
            pprint(name)
            pprint(alias)
            pprint(exceptions)

        if exceptions:
            tp, etag = cmk.create_timeperiod(name, alias, [], exceptions=exceptions)

            if args.debug:
                pprint(tp)

            if args.exclude_in:
                etp, etag = cmk.get_timeperiod(args.exclude_in)

                if args.debug:
                    pprint(etp)
                    pprint(etag)

                exclude = etp['extensions']['exclude']
                exclude.append(alias)

                if args.debug:
                    pprint(exclude)

                cmk.edit_timeperiod(args.exclude_in, etag, exclude=exclude)

            cmk.activate()
