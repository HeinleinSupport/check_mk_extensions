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
    u'title': _('Rspamd Scanned Messages'),
    u'unit': '1/s',
    u'color': '#000000',
}

metric_info['rspamd_ham_count_rate'] = {
    u'title': _('Rspamd HAM Messages'),
    u'unit': '1/s',
    u'color': '#00bb33',
}

metric_info['rspamd_spam_count_rate'] = {
    u'title': _('Rspamd SPAM Messages'),
    u'unit': '1/s',
    u'color': '#e70000',
}

metric_info['rspamd_actions_no_action_rate'] = {
    u'title': _('Rspamd No Action Taken'),
    u'unit': '1/s',
    u'color': '#00bb33',
}

metric_info['rspamd_actions_reject_rate'] = {
    u'title': _('Rspamd Rejected'),
    u'unit': '1/s',
    u'color': '#e70000',
}

metric_info['rspamd_actions_soft_reject_rate'] = {
    u'title': _('Rspamd Soft Rejected'),
    u'unit': '1/s',
    u'color': '#8c8c69',
}

metric_info['rspamd_actions_greylist_rate'] = {
    u'title': _('Rspamd Greylisted'),
    u'unit': '1/s',
    u'color': '#c9c977',
}

metric_info['rspamd_actions_rewrite_subject_rate'] = {
    u'title': _('Rspamd Subject Rewritten'),
    u'unit': '1/s',
    u'color': '#f3f35b',
}

metric_info['rspamd_actions_add_header_rate'] = {
    u'title': _('Rspamd Added Headers'),
    u'unit': '1/s',
    u'color': '#fafa0e',
}

graph_info.append({
    u'title': _('Rspamd HAM/SPAM'),
    u'metrics': [ ( 'rspamd_ham_count_rate', 'stacked' ),
                 ( 'rspamd_spam_count_rate', 'stacked' ),
                 ( 'rspamd_scanned_rate', 'line' ),
               ],
    })

graph_info.append({
    u'title': _('Rspamd Actions'),
    u'metrics': [ ( 'rspamd_actions_no_action_rate', 'stacked' ),
                 ( 'rspamd_actions_reject_rate', 'stacked' ),
                 ( 'rspamd_actions_soft_reject_rate', 'stacked' ),
                 ( 'rspamd_actions_greylist_rate', 'stacked' ),
                 ( 'rspamd_actions_rewrite_subject_rate', 'stacked' ),
                 ( 'rspamd_actions_add_header_rate', 'stacked' ),
                 ( 'rspamd_scanned_rate', 'line' ),
               ],
    })
