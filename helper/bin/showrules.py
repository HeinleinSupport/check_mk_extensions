#!/usr/bin/env python3

import sys
import argparse
import checkmkapi
import csv
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url', help='URL to Check_MK site')
parser.add_argument('-u', '--username', help='name of the automation user')
parser.add_argument('-p', '--password', help='secret of the automation user')
parser.add_argument('-D', '--debug', action='store_true', required=False)

args = parser.parse_args()

if args.debug:
    pprint(args)

wato = checkmkapi.CMKRESTAPI(args.url, args.username, args.password)

rulesets, etag = wato.get_rulesets()

lines = []
title = [
    'ruleset_name',
    'ruleset_title',
    'disabled',
    'rule_description',
    'rule_comment',
    'rule_url',
    'folder',
    'condition_hosttags',
    'condition_hostlabels',
    'condition_servicelabels',
    'condition_hostname',
    'condition_servicedesc',
    'value',
    'id'
]
lines.append(title)

for ruleset in rulesets.get('value', []):

    rules, etag = wato.get_rules(ruleset['id'])

    rulesetinfo = ruleset.get('extensions', {})

    for rule in rules.get('value', []):

        # pprint(rule)

        ruleinfo = rule.get('extensions', {})
        ruleproperties = ruleinfo.get('properties', {})

        conditions = ruleinfo.get('conditions', {})

        hostlabels = conditions.get('host_labels', [])
        hosttags = []
        for hosttag in conditions.get('host_tags', []):
            match hosttag['operator']:
                case 'is':
                    hosttags.append("%s is %s" % (hosttag['key'], hosttag['value']))
                case 'is_not':
                    hosttags.append("%s is not %s" % (hosttag['key'], hosttag['value']))
                case 'one_of':
                    hosttags.append("%s is one of %s" % (hosttag['key'], " or ".join(hosttag['value'])))
                case 'none_of':
                    hosttags.append("%s is none of %s" % (hosttag['key'], " or ".join(hosttag['value'])))
        servicelabels = conditions.get('service_labels', [])
        hostname = conditions.get('host_name', {})
        servicedesc = conditions.get('service_description', {})
        
        line = [
            rulesetinfo.get('name'),
            rulesetinfo.get('title'),
            ruleproperties.get('disabled', False),
            ruleproperties.get('description'),
            ruleproperties.get('comment'),
            ruleproperties.get('documentation_url'),
            ruleinfo.get('folder'),
            " and ".join(hosttags),
            " and ".join(map(lambda x: "%s%s:%s" % (("not " if x['operator'] == 'is_not' else ""), x['key'], x['value']), hostlabels)),
            " and ".join(map(lambda x: "%s%s:%s" % (("not " if x['operator'] == 'is_not' else ""), x['key'], x['value']), servicelabels)),
            "%s%s" % ("not " if hostname.get('operator') == 'none_of' else '', " or ".join(hostname.get('match_on', []))),
            "%s%s" % ("not " if servicedesc.get('operator') == 'none_of' else '', " or ".join(servicedesc.get('match_on', []))),
            ruleinfo.get('value_raw'),
            rule.get('id'),
        ]
        lines.append(line)

writer = csv.writer(sys.stdout, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer.writerows(lines)
