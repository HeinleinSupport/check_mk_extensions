#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2017 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

import argparse
import sys
from pprint import pprint, pformat

def percent255(rgbtuple):
    return map(lambda x: int(x*255), rgbtuple)

def tuple2hex(rgbtuple):
    return "#" + "".join(map(lambda x: chr(x).encode('hex'), rgbtuple))

def get_spaced_colors(n):
    max_value = 16581375 # 255**3
    interval = int(max_value / n)
    colors = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]
    
    return [(int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16)) for i in colors]

def get_hex_colors(n):
    return map(tuple2hex, get_spaced_colors(n))

defaultgraph = {'description': u'',
                'elements': [],
                'graph_options': {'consolidation_function': None,
                                  'explicit_vertical_range': (None, None),
                                  'omit_zero_metrics': False,
                                  'unit': ''},
                'hidden': True,
                'metrics': [],
                'name': '',
                'owner': '',
                'public': True,
                'title': u'',
                'topic': u'Metrics'}
defaultmetric = {'color': '#000000',
                 'expression': ('rrd',
                                'ox5.mailbox.org',
                                u'proc_OX',
                                'process_resident_size',
                                'max'), # max, min, ave
                 'line_type': 'line',
                 'title': u'OX5 Process Resident Size',
                 'visible': True}

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True, help='user_custom_graph filename')
parser.add_argument('-o', '--overwrite', action="store_true", help="overwrite existing graphs")
exgroup = parser.add_mutually_exclusive_group()
exgroup.add_argument('-2', '--two', action="store_true", help='one graph per host with services as pairs')
exgroup.add_argument('-3', '--three', action="store_true", help='one graph per service for multiple hosts')
parser.add_argument('-t', '--topic', help='Topic for the graph(s)')
parser.add_argument('-n', '--name', required=True, nargs='*')
parser.add_argument('-T', '--title', required=True, nargs='*')
parser.add_argument('-H', '--host', required=True, nargs='*', help='Hostname(s)')
parser.add_argument('-s', '--service', required=True, nargs='*', help='Service Description:Data Source:Metric (max, min, ave):Unit:Line Type')

args = parser.parse_args()

if len(args.title) != len(args.name):
    print "The lists of Names and Titles have to match in length"
    sys.exit(1)

customgraphs = eval(file(args.file).read())

if args.two:
    # one graph per host with services as pairs
    hostlen = len(args.host)
    if hostlen != len(args.name):
        print "The lists of Hosts and Names have to match in length"
        sys.exit(1)

    colors = get_hex_colors(len(args.service) / 2)
    for i in xrange(hostlen):
        name = args.name[i]
        if not args.overwrite and name in customgraphs:
            print "%s already in file" % name
            sys.exit()
        customgraphs[name] = defaultgraph.copy()
        customgraphs[name]['metrics'] = []
        customgraphs[name]['name'] = name
        customgraphs[name]['title'] = args.title[i]
        customgraphs[name]['graph_options']['unit'] = args.service[0].split(':')[3] # first service defines unit
        if args.topic:
            customgraphs[name]['topic'] = args.topic
        for j in xrange(len(args.service)):
            desc, ds, data, unit, linetype = args.service[j].split(':')
            metric = defaultmetric.copy()
            metric['color'] = colors[j / 2]
            metric['expression'] = ('rrd', args.host[i], desc, ds, data)
            metric['line_type'] = linetype
            metric['title'] = '%s %s %s' % (args.host[i].split('.')[0], desc, ds)
            customgraphs[name]['metrics'].append(metric)
    
if args.three:
    # one graph per service for multiple hosts
    servicelen = len(args.service)
    if servicelen != len(args.name):
        print "The lists of Services and Names have to match in length"
        sys.exit(1)
    
    hostcolor = {}
    colors = get_hex_colors(len(args.host))
    for i in xrange(len(args.host)):
        hostcolor[args.host[i]] = colors[i]

    for i in xrange(servicelen):
        name = args.name[i]
        desc, ds, data, unit, linetype = args.service[i].split(':')

        if name in customgraphs:
            print "%s already in file"
            sys.exit()
        customgraphs[name] = defaultgraph.copy()
        customgraphs[name]['metrics'] = []
        customgraphs[name]['name'] = name
        customgraphs[name]['title'] = args.title[i]
        customgraphs[name]['graph_options']['unit'] = unit
        if args.topic:
            customgraphs[name]['topic'] = args.topic
        for host in args.host:
            metric = defaultmetric.copy()
            metric['color'] = hostcolor[host]
            metric['expression'] = ('rrd', host, desc, ds, data)
            metric['line_type'] = linetype
            metric['title'] = '%s %s' % (host.split('.')[0], desc)
            customgraphs[name]['metrics'].append(metric)

pprint(customgraphs)
