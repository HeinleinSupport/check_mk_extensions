#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2016 Heinlein Support GmbH
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

metric_info['amavis_child_avail'] = {
    'title': _('Available Amavis Child Processes'),
    'unit': 'count',
    'color': '#90ee90',
}
# amavis_ContentCleanMsgs=0;;;; amavis_ContentSpamMsgs=0;;;; amavis_ContentVirusMsgs=0;;;; amavis_InMsgs=0;;;; amavis_OutMsgs=0;;;; amavis_OutMsgsAttemptFails=0;;;; amavis_InMsgsStatusRejectedOriginating

metric_info['amavis_ContentCleanMsgs'] = {
    'title': _('Amavis Clean Messages'),
    'unit': '1/s',
    'color': '#90ee90',
}

metric_info['amavis_InMsgs'] = {
    'title': _('Amavis In Messages'),
    'unit': '1/s',
    'color': '#90ee90',
}

metric_info['amavis_OutMsgs'] = {
    'title': _('Amavis Out Messages'),
    'unit': '1/s',
    'color': '#90ee90',
}

metric_info['amavis_ContentSpamMsgs'] = {
    'title': _('Amavis Spam Messages'),
    'unit': '1/s',
    'color': '#ffa500',
}

metric_info['amavis_ContentVirusMsgs'] = {
    'title': _('Amavis Virus Messages'),
    'unit': '1/s',
    'color': '#ff6347',
}

metric_info['amavis_OutMsgsAttemptFails'] = {
    'title': _('Amavis Failed Out Attempts'),
    'unit': '1/s',
    'color': '#ff6347',
}

metric_info['amavis_InMsgsStatusRejectedOriginating'] = {
    'title': _('Amavis Rejected Originating In Messages'),
    'unit': '1/s',
    'color': '#ff6347',
}
