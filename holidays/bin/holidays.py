#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2023 Heinlein Support GmbH - License: GNU General Public License v2
# Robert Sander <r.sander@heinlein-support.de>
#

import sys
import os
import argparse
import checkmkapi
import requests
import json
from datetime import date
from pprint import pprint

apifeiertage = 'https://get.api-feiertage.de/'

#
# defaults
#
countries = ["de"]
default_country = "de"
states  = {
    'de': {
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
    },
}
always = [{'day': 'all', 'time_ranges': [{'start': '00:00', 'end': '24:00'}]}]


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url', help='URL to Check_MK site')
parser.add_argument('-u', '--username', help='name of the automation user')
parser.add_argument('-p', '--password', help='secret of the automation user')
parser.add_argument('-c', '--config-file', help='config file (JSON)',
                    default=os.path.join(os.environ.get('OMD_ROOT'), 'etc', 'holidays'))
parser.add_argument('-D', '--debug', action='store_true')
subparsers = parser.add_subparsers(title='available commands', help='call "subcommand --help" for more information')
delete_timeperiod = subparsers.add_parser('delete', help='delete timeperiod')
delete_timeperiod.set_defaults(func='delete_timeperiod')
delete_timeperiod.add_argument('name', help='name of timeperiod')
delete_old = subparsers.add_parser('delete_old', help='delete old holiday timeperiods')
delete_old.set_defaults(func='delete_old')
dump_timeperiods = subparsers.add_parser('dump', help='dump timeperiods')
dump_timeperiods.set_defaults(func='dump_timeperiods')
add_holidays = subparsers.add_parser('add_holidays', help='add timeperiod from api-feiertage.de')
add_holidays.set_defaults(func='add_holidays')
add_holidays.add_argument('-a', '--all-states', action='store_true', help='Nur bundesweite Feiertage')
add_holidays.add_argument('-l', '--country', choices=countries, default=default_country, help='Land (default=de)')
add_holidays.add_argument('-s', '--state', choices=states[default_country].keys(), help='Bundesland')
add_holidays.add_argument('-y', '--year')
add_holidays.add_argument('-Y', '--current-year', action='store_true')
add_holidays.add_argument('-e', '--exclude-in-default', action='store_true', help='Exclude in passender Standard-Timeperiod')
add_holidays.add_argument('-E', '--exclude-in', help='Exclude in anderer Timeperiod')
add_region = subparsers.add_parser('add_region', help='add a new region to the configuration (base timeperiods and tag)')
add_region.set_defaults(func='add_region')
add_region.add_argument('-l', '--country', choices=countries, default=default_country, help='Land')
add_region.add_argument('-s', '--state', choices=states['de'].keys(), help='Bundesland', required=True)
add_auto_holidays = subparsers.add_parser('add_auto_holidays', help='add timeperiods from api-feiertage.de for all regions')
add_auto_holidays.set_defaults(func='add_auto_holidays')
add_auto_holidays.add_argument('-y', '--year')
add_auto_holidays.add_argument('-Y', '--current-year', action='store_true')
cleanup = subparsers.add_parser('cleanup', help='remove timeperiods and tag group. Use with caution!')
cleanup.set_defaults(func='cleanup')

def exclude_in_timeperiod(name, exclude_in_tp):
    etp, etag = cmk.get_timeperiod(exclude_in_tp)

    if args.debug:
        pprint(etp)
        pprint(etag)

    exclude = etp['extensions']['exclude']
    exclude.append(name)

    if args.debug:
        pprint(exclude)

    cmk.edit_timeperiod(exclude_in_tp, etag, exclude=exclude)

def add_holiday_timeperiod(country=default_country, state=None, all_states=False, current_year=False, set_year=None, exclude_in_default=True, exclude_in=None):
    params = {}
    name = config['timeperiods']['holidays']['name'] + '_'
    alias = config['timeperiods']['holidays']['title'] + ' '
    year = None
    if current_year:
        year = str(date.today().year)
    elif set_year:
        year = set_year
    if year:
        params['years'] = year
        name += year
        alias += year
    name += "_" + country
    alias += " " + country.upper()
    if all_states:
        params['all_states'] = "true"
        name += '_bundeseinheitlich'
        alias += ' bundeseinheitlich'
    elif state:
        params['states'] = state
        name += '_%s' % state
        alias += ' %s' % states[country][state]

    if args.debug:
        pprint(params)

    if not params:
        print('Please give at least a year or a state.\n')
        add_holidays.print_help()
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

    if data.get('feiertage'):
        exceptions = []
        for feiertag in data['feiertage']:
            exceptions.append({
                'date': feiertag['date'],
                'time_ranges': [ { 'start': '00:00:00', 'end': '24:00:00' } ]
            })

        if args.debug:
            pprint(name)
            pprint(alias)
            pprint(exceptions)

        if exceptions:
            tp, etag = cmk.create_timeperiod(name, alias, [], exceptions=exceptions)

            if args.debug:
                pprint(tp)

            if exclude_in_default:
                exclude_in_timeperiod(name, config['timeperiods']['workhours']['name'] + "_" + country + "_" + state)
                
            if exclude_in:
                exclude_in_timeperiod(name, exclude_in)
    else:
        print('Error: %s' % data.get('additional_note'))
        sys.exit(1)

args = parser.parse_args()
if 'func' not in args:
    parser.print_help()
    sys.exit(1)
if args.debug:
    pprint(args)

config = json.load(open(args.config_file))

if args.debug:
    pprint(config)

cmk = checkmkapi.CMKRESTAPI(args.url, args.username, args.password)

if args.func == 'dump_timeperiods':
    pprint(cmk.get_timeperiods()[0])

if args.func == 'delete_timeperiod':
    cmk.delete_timeperiod(args.name, '*')
    cmk.activate()

if args.func == 'delete_old':
    tps, etag = cmk.get_timeperiods()

    to_delete = []
    thisyear = str(date.today().year)

    if args.debug:
        print(f"Removing each timeperiod starting with \"{config['timeperiods']['holidays']['name']}_\" up to but not including {thisyear}")

    tps, etag = cmk.get_timeperiods()

    for tp in tps['value']:
        if tp['id'].startswith(config['timeperiods']['holidays']['name'] + '_'):
            year = tp['id'].split('_')[1]
            if year < thisyear:
                to_delete.append(tp['id'])

    for tp in tps['value']:
        excludes = tp['extensions'].get('exclude', [])
        changes = False
        for td in to_delete:
            if td in excludes:
                if args.debug:
                    print(f"Removing {td} from {tp['id']}")
                excludes.remove(td)
                changes = True
        if changes:
            te, etag = cmk.get_timeperiod(tp['id'])
            cmk.edit_timeperiod(tp['id'], etag, exclude=excludes)
    for td in to_delete:
        if args.debug:
            print(f"Removing {td}")
        cmk.delete_timeperiod(td, '*')
    if to_delete:
        cmk.activate()

if args.func == 'add_holidays':
    add_holiday_timeperiod(args.country, args.state, args.all_states, args.current_year, args.year, args.exclude_in_default, args.exclude_in)
    cmk.activate()

if args.func == "add_region":
    workhoursname = '%s_%s_%s' % ( config['timeperiods']['workhours']['name'],
                                   args.country,
                                   args.state )
    tp, etag = cmk.create_timeperiod(workhoursname,
                                     '%s %s %s' % ( config['timeperiods']['workhours']['title'],
                                                    args.country.upper(),
                                                    states[args.country][args.state] ),
                                     config['workdays'])
    if args.debug:
        pprint(tp)
        
    tp, etag = cmk.create_timeperiod('%s_%s_%s' % ( config['timeperiods']['oncall']['name'],
                                                    args.country,
                                                    args.state ),
                                     '%s %s %s' % ( config['timeperiods']['oncall']['title'],
                                                    args.country.upper(),
                                                    states[args.country][args.state] ),
                                     always,
                                     exclude=[workhoursname])
    if args.debug:
        pprint(tp)

    add_holiday_timeperiod(country=args.country, state=args.state, current_year=True)

    tg = None
    try:
        tg, etag = cmk.get_host_tag_group(config['taggroup']['name'])
    except:
        pass

    if tg:
        tags = tg['extensions']['tags']

        tags.append({'ident': "%s_%s_%s" % (config['taggroup']['name'], args.country, args.state),
                     'title': "%s %s %s" % (config['taggroup']['title'], args.country.upper(), states[args.country][args.state])})

        cmk.edit_host_tag_group(config['taggroup']['name'], etag, tags=tags)

    else:
        tg, etag = cmk.create_host_tag_group(
            config['taggroup']['name'],
            config['taggroup']['title'],
            [
                {'title': config['taggroup']['empty_title']},
                {'ident': "%s_%s_%s" % (config['taggroup']['name'],
                                     args.country,
                                     args.state),
                 'title': "%s %s %s" % (config['taggroup']['title'],
                                        args.country.upper(),
                                        states[args.country][args.state])}
            ],
            topic = config['taggroup'].get('topic'),
            help = config['taggroup'].get('help')
        )
        
    cmk.activate()
    
if args.func == 'add_auto_holidays':
    tps, etag = cmk.get_timeperiods()
    changes = False
    for tp in tps['value']:
        if tp['id'].startswith(config['timeperiods']['workhours']['name']):
            if args.debug:
                print(f"found {tp['id']}")
            _, country, state = tp['id'].split('_')
            add_holiday_timeperiod(country=country, state=state, current_year=args.current_year, set_year=args.year)
            changes = True
    if changes:
        cmk.activate()

if args.func == "cleanup":
    tps, etag = cmk.get_timeperiods()

    if args.debug:
        pprint(tps)

    changes = False
        
    for typ in ['oncall', 'workhours', 'holidays']:
        # order is important
        for tp in tps['value']:
            if tp['id'].startswith(config['timeperiods'][typ]['name']):
                if args.debug:
                    print(f"removing {tp['id']}")
                cmk.delete_timeperiod(tp['id'], '*')
                changes = True

    try:
        cmk.delete_host_tag_group(config['taggroup']['name'])
        if args.debug:
            print(f"remove host tag group {config['taggroup']['name']}")
        changes = True
    except:
        pass
    
    if changes:
        cmk.activate()
