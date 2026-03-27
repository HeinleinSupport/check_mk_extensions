#!/usr/bin/env python3
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


from cmk.graphing.v1 import Title, graphs, metrics

UNIT_PER_SECOND = metrics.Unit(metrics.DecimalNotation('/s'))

metric_rspamd_scanned_rate = metrics.Metric(
    name='rspamd_scanned_rate',
    title=Title("Rspamd Scanned Messages"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.BLACK,
)

metric_rspamd_ham_count_rate = metrics.Metric(
    name='rspamd_ham_count_rate',
    title=Title("Rspamd HAM Messages"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.DARK_GREEN,
)

metric_rspamd_spam_count_rate = metrics.Metric(
    name='rspamd_spam_count_rate',
    title=Title("Rspamd SPAM Messages"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.DARK_RED,
)

metric_rspamd_actions_no_action_rate = metrics.Metric(
    name='rspamd_actions_no_action_rate',
    title=Title("Rspamd No Action Taken"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.DARK_GREEN,
)

metric_rspamd_actions_reject_rate = metrics.Metric(
    name='rspamd_actions_reject_rate',
    title=Title("Rspamd Rejected"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.DARK_RED,
)

metric_rspamd_actions_soft_reject_rate = metrics.Metric(
    name='rspamd_actions_soft_reject_rate',
    title=Title("Rspamd Soft Rejected"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.DARK_GRAY,
)

metric_rspamd_actions_greylist_rate = metrics.Metric(
    name='rspamd_actions_greylist_rate',
    title=Title("Rspamd Greylisted"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.LIGHT_BROWN,
)

metric_rspamd_actions_rewrite_subject_rate = metrics.Metric(
    name='rspamd_actions_rewrite_subject_rate',
    title=Title("Rspamd Subject Rewritten"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.LIGHT_YELLOW,
)

metric_rspamd_actions_add_header_rate = metrics.Metric(
    name='rspamd_actions_add_header_rate',
    title=Title("Rspamd Added Headers"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.YELLOW,
)

graph_rspamd_ham_spam = graphs.Graph(
    name='rspamd_ham_spam',
    title=Title("Rspamd HAM/SPAM"),
    compound_lines=[
        'rspamd_ham_count_rate',
        'rspamd_spam_count_rate',
    ],
    simple_lines=['rspamd_scanned_rate'],
)

graph_rspamd_actions = graphs.Graph(
    name='rspamd_actions',
    title=Title("Rspamd Actions"),
    compound_lines=[
        'rspamd_actions_no_action_rate',
        'rspamd_actions_reject_rate',
        'rspamd_actions_soft_reject_rate',
        'rspamd_actions_greylist_rate',
        'rspamd_actions_rewrite_subject_rate',
        'rspamd_actions_add_header_rate',
    ],
    simple_lines=['rspamd_scanned_rate'],
)

graph_rspamd_percentage = graphs.Graph(
    name="rspamd_spam_percentage",
    title=Title("SPAM in Relation to Total"),
    simple_lines=[metrics.Fraction(
            title=Title("SPAM Percentage"),
            unit=UNIT_PERCENTAGE,
            color=metrics.Color.RED,
            dividend=metrics.Product(
                title=Title("SPAM times one hundred"),
                unit=UNIT_PERCENTAGE,
                color=metrics.Color.RED,
                factors=[
                    "rspamd_spam_count_rate",
                    metrics.Constant(
                        title=Title("One hundred"),
                        unit=UNIT_PERCENTAGE,
                        color=metrics.Color.RED,
                        value=100.0,
                    )
            ]),
            divisor="rspamd_scanned_rate",
    )],
)
