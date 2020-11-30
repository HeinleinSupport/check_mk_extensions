#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2018 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

metric_info['rspamd_scanned_rate'] = {
    'title': _('Rspamd Scanned Messages'),
    'unit': '1/s',
    'color': '#000000',
}

metric_info['rspamd_ham_count_rate'] = {
    'title': _('Rspamd HAM Messages'),
    'unit': '1/s',
    'color': '#00bb33',
}

metric_info['rspamd_spam_count_rate'] = {
    'title': _('Rspamd SPAM Messages'),
    'unit': '1/s',
    'color': '#e70000',
}

metric_info['rspamd_actions_no_action_rate'] = {
    'title': _('Rspamd No Action Taken'),
    'unit': '1/s',
    'color': '#00bb33',
}

metric_info['rspamd_actions_reject_rate'] = {
    'title': _('Rspamd Rejected'),
    'unit': '1/s',
    'color': '#e70000',
}

metric_info['rspamd_actions_soft_reject_rate'] = {
    'title': _('Rspamd Soft Rejected'),
    'unit': '1/s',
    'color': '#8c8c69',
}

metric_info['rspamd_actions_greylist_rate'] = {
    'title': _('Rspamd Greylisted'),
    'unit': '1/s',
    'color': '#c9c977',
}

metric_info['rspamd_actions_rewrite_subject_rate'] = {
    'title': _('Rspamd Subject Rewritten'),
    'unit': '1/s',
    'color': '#f3f35b',
}

metric_info['rspamd_actions_add_header_rate'] = {
    'title': _('Rspamd Added Headers'),
    'unit': '1/s',
    'color': '#fafa0e',
}

graph_info.append({
    'title': _('Rspamd HAM/SPAM'),
    'metrics': [ ( 'rspamd_ham_count_rate', 'stack' ),
                 ( 'rspamd_spam_count_rate', 'stack' ),
                 ( 'rspamd_scanned_rate', 'line' ),
               ],
    })

graph_info.append({
    'title': _('Rspamd Actions'),
    'metrics': [ ( 'rspamd_actions_no_action_rate', 'stack' ),
                 ( 'rspamd_actions_reject_rate', 'stack' ),
                 ( 'rspamd_actions_soft_reject_rate', 'stack' ),
                 ( 'rspamd_actions_greylist_rate', 'stack' ),
                 ( 'rspamd_actions_rewrite_subject_rate', 'stack' ),
                 ( 'rspamd_actions_add_header_rate', 'stack' ),
                 ( 'rspamd_scanned_rate', 'line' ),
               ],
    })
