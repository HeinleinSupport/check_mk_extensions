#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.utils.type_defs import UserId
from cmk.gui.i18n import _
from cmk.gui.type_defs import (
    ColumnSpec,
    PainterParameters,
    SorterSpec,
    VisualLinkSpec,
)
from cmk.gui.views.store import multisite_builtin_views


multisite_builtin_views.update(
    {
        'hostparents': {
            'link_from': {},
            'packaged': False,
            'single_infos': [],
            'name': 'host_parents',
            'title': _('Host and Parents'),
            'owner': UserId.builtin(),
            'topic': 'heinlein',
            'sort_index': 99,
            'is_show_more': False,
            'description': '',
            'icon': None,
            'add_context_to_title': True,
            'hidden': False,
            'hidebutton': True,
            'public': True,
            'datasource': 'hosts',
            'browser_reload': 0,
            'layout': 'table',
            'num_columns': 1,
            'column_headers': 'pergroup',
            'painters': [
                ColumnSpec(
                    name='host',
                    parameters=PainterParameters(color_choices=[]),
                    link_spec=VisualLinkSpec(type_name='views', name='host'),
                    tooltip=None,
                ),
                ColumnSpec(name='host_parents',),
                ColumnSpec(
                    name='svc_plugin_output',
                    join_value='ESX Hostsystem',
                    column_title='VMware',
                    # column_type='join_column',
                ),
                ColumnSpec(
                    name='svc_plugin_output',
                    join_value='Proxmox VE VM Info',
                    column_title='Proxmox',
                    #'column_type': 'join_column'}],
                ),
            ],
            'group_painters': [],
            'sorters': [
                SorterSpec(sorter='host_name', negate=False),
            ],
            'context': {
                'host_labels': {
                    'host_labels_indexof_@!@': '',
                    'host_labels_orig_indexof_@!@': '',
                    'host_labels_@!@_bool': 'and',
                    'host_labels_@!@_vs_indexof_@:@': '',
                    'host_labels_@!@_vs_orig_indexof_@:@': '',
                    'host_labels_@!@_vs_@:@_bool': 'and',
                    'host_labels_@!@_vs_count': '1',
                    'host_labels_@!@_vs_indexof_1': '1',
                    'host_labels_@!@_vs_orig_indexof_1': '1',
                    'host_labels_@!@_vs_1_bool': 'and',
                    'host_labels_count': '1',
                    'host_labels_indexof_1': '1',
                    'host_labels_orig_indexof_1': '1',
                    'host_labels_1_bool': 'and',
                    'host_labels_1_vs_indexof_@:@': '',
                    'host_labels_1_vs_orig_indexof_@:@': '',
                    'host_labels_1_vs_@:@_bool': 'and',
                    'host_labels_1_vs_count': '1',
                    'host_labels_1_vs_indexof_1': '1',
                    'host_labels_1_vs_orig_indexof_1': '1',
                    'host_labels_1_vs_1_bool': 'and'
                },
                'hostregex': {'host_regex': '', 'neg_host_regex': ''},
                'siteopt': {'site': ''},
                'wato_folder': {'wato_folder': ''}
            }
        }
    }
) 
