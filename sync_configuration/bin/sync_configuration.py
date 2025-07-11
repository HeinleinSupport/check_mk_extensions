#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2025 Heinlein Consulting GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

from collections.abc import Mapping # type: ignore
from typing import Any # type: ignore

import argparse # type: ignore
import re # type: ignore
from pprint import pprint # type: ignore

import checkmkapi

from cmk.utils import password_store


def url_to_site(url):
    return url.split('/')[3]


def get_aux_tags(wato: checkmkapi.CMKRESTAPI, sync_tag: str) -> Mapping[str, Any]:
    aux_tags = {}
    if args.verbose:
        print(f'getting aux tags from {url_to_site(wato._api_url)}')
    result, etag = wato.get_aux_tags()
    for aux_tag_data in result.get('value', []):
        if aux_tag_data['id'].startswith(sync_tag):
            aux_tags[aux_tag_data['id']] = aux_tag_data['extensions']
            aux_tags[aux_tag_data['id']]['title'] = aux_tag_data['title']
    if args.debug:
        pprint(aux_tags)
    return aux_tags


def get_tag_groups(wato, sync_tag):
    tag_groups = {}
    if args.verbose:
        print(f'getting tag groups from {url_to_site(wato._api_url)}')
    result, etag = wato.get_host_tag_groups()
    for tag_group_data in result.get('value', []):
        if tag_group_data['id'].startswith(sync_tag):
            tag_groups[tag_group_data['id']] = tag_group_data['extensions']
            tag_groups[tag_group_data['id']]['title'] = tag_group_data['title']
    if args.debug:
        pprint(tag_groups)
    return tag_groups


def get_rulesets(wato):
    rulesets = set()
    if args.verbose:
        print(f'getting rulesets from {url_to_site(wato._api_url)}')
    result, etag = wato.search_rulesets(folder='~')
    for ruleset_data in result.get('value', []):
        rulesets.add(ruleset_data['id'])
    if args.debug:
        pprint(rulesets)
    return rulesets


def get_rules(wato, ruleset, sync_tag, central = True):
    rules = {}
    sort_order = {}
    if args.verbose:
        print(f'getting rules in {ruleset} from {url_to_site(wato._api_url)}')
    result, etag = wato.get_rules(ruleset)
    for rule_data in result.get('value', []):
        ext = rule_data.get('extensions', {})
        folder = ext.get('folder')
        if f'[{sync_tag}' in rule_data['title'] and folder == '/':
            if central:
                rule_ident = rule_data['id']
            else:
                match = regex_rule_title_id.match(rule_data['title'])
                try:
                    rule_ident = match.group(1)
                except AttributeError:
                    pprint(rule_data)
                    raise
            if rule_ident in rules:
                raise RuntimeError(f'rule description {rule_data["title"]} already exists')
            sort_order[int(ext['folder_index'])] = rule_ident
            del ext['folder_index']
            del ext['properties']['description']
            rule_tmp = {
                'title': rule_data['title'],
                'ext': ext,
                'id': rule_data['id'],
            }
            rules[rule_ident] = rule_tmp
    rule_relations = {}
    for key, rule_ident in sort_order.items():
        rule_relation = {}
        for i in range(key-1, -1, -1):
            if i in sort_order:
                rule_relation['after'] = sort_order[i]
                break
        if rule_relation:
            rule_relations[rule_ident] = rule_relation
    if args.debug:
        pprint(rules)
        pprint(rule_relations)
    return rules, rule_relations


def get_notification_rules(wato, sync_tag, central = True):
    rules = {}
    if args.verbose:
        print(f'getting notification rules from {url_to_site(wato._api_url)}')
    result, etag = wato.get_all_notification_rules()
    if args.debug:
        pprint(result)


def sync_aux_tags(site_id, site_data, changes):
    site_aux_tags = get_aux_tags(site_data['wato'], args.sync)
    for aux_tag, aux_tag_data in central_aux_tags.items():
        if aux_tag in site_aux_tags:
            if aux_tag_data != site_aux_tags[aux_tag]:
                if args.verbose:
                    print(f'updating aux tag {aux_tag} on {site_id}')
                site_data['wato'].edit_aux_tag(
                    aux_tag,
                    aux_tag_data.get('title'),
                    aux_tag_data.get('topic'),
                    aux_tag_data.get('help')
                )
                changes = True
            del site_aux_tags[aux_tag]
        else:
            if args.verbose:
                print(f'adding aux tag {aux_tag} to {site_id}')
            site_data['wato'].create_aux_tag(
                aux_tag,
                aux_tag_data.get('title'),
                aux_tag_data.get('topic'),
                aux_tag_data.get('help')
            )
            changes = True
    for site_aux_tag in site_aux_tags:
        if args.verbose:
            print(f'removing aux tag {site_aux_tag} from {site_id}')
        site_data['wato'].delete_aux_tag(site_aux_tag)
        changes = True
    return changes


def sync_tag_groups(site_id, site_data, changes):
    site_tag_groups = get_tag_groups(site_data['wato'], args.sync)
    for tag_group, tag_group_data in central_tag_groups.items():
        if tag_group in site_tag_groups:
            if tag_group_data != site_tag_groups[tag_group]:
                if args.verbose:
                    print(f'Updating tag group {tag_group} on {site_id}')
                site_data['wato'].edit_host_tag_group(
                    tag_group,
                    '"*"',  # override etag
                    tag_group_data.get('title'),
                    tag_group_data.get('topic'),
                    tag_group_data.get('help'),
                    tag_group_data.get('tags'),
                )
                changes = True
            del site_tag_groups[tag_group]
        else:
            if args.verbose:
                print(f'Adding tag group {tag_group} to {site_id}')
            site_data['wato'].create_host_tag_group(
                tag_group,
                tag_group_data.get('title'),
                tag_group_data.get('tags'),
                tag_group_data.get('topic'),
                tag_group_data.get('help'),
            )
            changes = True
    for site_tag_group in site_tag_groups:
        if args.verbose:
            print(f'removing tag group {site_tag_group} from {site_id}')
        site_data['wato'].delete_host_tag_group(site_tag_group)
        changes = True
    return changes


def sync_rules(site_id, site_data, changes):
    site_rulesets = get_rulesets(site_data['wato'])
    
    if args.debug:
        print(f"merged_rulesets = {central_rulesets.union(site_rulesets)}")

    for ruleset in central_rulesets.union(site_rulesets):
        site_rules, site_relations = get_rules(
            site_data['wato'],
            ruleset,
            args.sync,
            central = False,
        )
        delete_rules = [x['id'] for x in site_rules.values()]
        if args.debug:
            print(f"site_rules: {site_rules}")
            print(f"site_relations: {site_relations}")
            print(f"delete_rules: {delete_rules}")
        for rule_ident, rule_data in central_rules.get(ruleset, {}).items():
            if rule_ident in site_rules:
                delete_rules.remove(site_rules[rule_ident]['id'])
                if rule_data['ext'] != site_rules[rule_ident]['ext']:
                    if args.verbose:
                        print(f'updating rule "{rule_data["title"]}" in {ruleset} on {site_id}')
                    properties = rule_data['ext'].get('properties', {})
                    m = regex_rule_title.match(rule_data['title'])
                    properties['description'] = f'{m.group(1)}[{args.sync}-{rule_ident}]{m.group(2)}'
                    if args.debug:
                        print('rule_data')
                        pprint(rule_data['ext'])
                        pprint(site_rules[rule_ident]['ext'])
                        pprint(properties)
                        pprint(rule_data['ext'].get('conditions', {}))
                    site_data['wato'].edit_rule(
                        site_rules[rule_ident]['id'],
                        '"*"',
                        rule_data['ext'].get('value_raw', ''),
                        rule_data['ext'].get('conditions', {}),
                        properties,
                    )
                    changes = True
            else:
                if args.verbose:
                    print(f'adding rule "{rule_data["title"]}" in {ruleset} to {site_id}')
                properties = rule_data['ext'].get('properties', {})
                m = regex_rule_title.match(rule_data['title'])
                properties['description'] = f'{m.group(1)}[{args.sync}-{rule_ident}]{m.group(2)}'
                site_rule, etag = site_data['wato'].create_rule(
                    ruleset,
                    rule_data['ext'].get('folder', '/'),
                    rule_data['ext'].get('value_raw', ''),
                    rule_data['ext'].get('conditions', {}),
                    properties,
                )
                site_rules[rule_ident] = {
                    'title': site_rule['title'],
                    'ext': site_rule['extensions'],
                    'id': site_rule['id'],
                }
                changes = True
        for rule_ident, relation in central_relations.get(ruleset, {}).items():
            site_relation = site_relations.get(rule_ident, {})
            if relation.get('after') != site_relation.get('after'):
                if args.verbose:
                    print(f'moving rule "{central_rules[ruleset][rule_ident]["title"]}" ({site_rules[rule_ident]["id"]}) after "{central_rules[ruleset][relation["after"]]["title"]}" ({site_rules[relation["after"]]["id"]}) in {ruleset} on {site_id}')
                site_data['wato'].move_rule(
                    site_rules[rule_ident]['id'],
                    '"*"',
                    'after_specific_rule',
                    neighbor_id=site_rules[relation['after']]['id'],
                )
                changes = True
        for site_rule_id in delete_rules:
            if args.verbose:
                print(f'removing rule {site_rule_id} in {ruleset} from {site_id}')
            site_data['wato'].delete_rule(site_rule_id)
            changes = True
        
    return changes

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url', help='URL to central Check_MK site')
parser.add_argument('-u', '--username', help='name of the automation user')
parser.add_argument('-p', '--password', help='secret of the automation user')
parser.add_argument('-t', '--sync', help='Sync Tag', required=True)
parser.add_argument('-v', '--verbose', action='store_true', required=False)
parser.add_argument('-D', '--debug', action='store_true', required=False)

args = parser.parse_args()

if args.debug:
    pprint(args)

regex_rule_title_id = re.compile(f'.*\\[{args.sync}-([^]]+)\\].*')
regex_rule_title = re.compile(f'(.*)\\[{args.sync}\\](.*)')

sites = {}

central_wato = checkmkapi.CMKRESTAPI(args.url, args.username, args.password)

if args.verbose:
    print(f'getting sites from {url_to_site(central_wato._api_url)}')
result, etag = central_wato.get_all_site_connections()
for site in result.get('value', []):
    site_data = site.get('extensions', {})
    if args.debug:
        pprint(site_data)
    status = site_data.get('status_connection', {})
    if status.get('disable_in_status_gui', False):
        continue
    connection = status.get('connection', {})
    if connection.get('socket_type') == 'local':
        continue
    site_id = site_data.get('basic_settings', {}).get('site_id')
    if site_id:
        sites[site_id] = {
            'url': status.get('url_prefix'),
        }
        if 'host' in connection:
            sites[site_id]['host'] = connection['host']
        if 'path' in connection:
            sites[site_id]['path'] = connection['path']

remove_sites = []

for site_id in sites:
    if args.verbose:
        print(f'getting automation secret for {site_id}')

    try:
        pw = password_store.lookup(
            pw_id=f'site_{site_id}',
            pw_file=password_store.password_store_path()
        )
    except ValueError:
        remove_sites.append(site_id)
        continue

    sites[site_id]['wato'] = checkmkapi.CMKRESTAPI(
        sites[site_id]['url'],
        'automation',
        pw
    )
for site in remove_sites:
    del sites[site_id]

if args.debug:
    pprint(sites)

central_aux_tags = get_aux_tags(central_wato, args.sync)

central_tag_groups = get_tag_groups(central_wato, args.sync)

# central_passwords = get_passwords(central_wato, args.sync)

central_rulesets = get_rulesets(central_wato)

central_rules = {}
central_relations = {}
for ruleset in central_rulesets:
    result1, result2 = get_rules(central_wato, ruleset, args.sync)
    if result1:
        central_rules[ruleset] = result1
        central_relations[ruleset] = result2

# central_notification_rules = get_notification_rules(central_wato, args.sync)

for site_id, site_data in sites.items():
    changes = False

    changes = sync_aux_tags(site_id, site_data, changes)
    
    changes = sync_tag_groups(site_id, site_data, changes)

    changes = sync_rules(site_id, site_data, changes)

    if changes:
        if args.verbose:
            print(f'activating changes on {site_id}')
        site_data['wato'].activate()
