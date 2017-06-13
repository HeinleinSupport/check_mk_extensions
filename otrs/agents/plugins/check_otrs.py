#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2015 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

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

import ConfigParser
import MySQLdb
import os

cfg = ConfigParser.SafeConfigParser()
# make option names case sensitive
# http://docs.python.org/library/configparser.html#ConfigParser.RawConfigParser.optionxform
cfg.optionxform = str

try:
    cfgdir = os.environ['MK_CONFDIR']
except KeyError:
    cfgdir = '/etc/check_mk'

cfg.read(os.path.join(cfgdir, 'otrs.cfg'))
defaults = cfg.defaults()

db = MySQLdb.connect(defaults['dbhost'], defaults['dbuser'], defaults['dbpass'], defaults['dbname'])
cur = db.cursor()

# fetch state names
ticket_state = {}
cur.execute('SELECT `id`, `name` FROM `ticket_state`')
rows = cur.fetchall()
for row in rows:
    ticket_state[row[0]] = row[1]

print '<<<otrs>>>'

for section in cfg.sections():
    queuename = section.replace(' ', '_')
    if cfg.has_option(section, 'types'):
        types = cfg.get(section, 'types')
        if types != '':
            for typeid in types.split():
                cur.execute("SELECT COUNT(*) FROM `ticket` WHERE `queue_id` = '%s' AND `ticket_state_id` = '%s'" % (cfg.get(section, 'id'), typeid))
                count = cur.fetchone()[0]
                print queuename, typeid, count, ticket_state[int(typeid)]
        else:
            cur.execute("SELECT COUNT(*) FROM `ticket` WHERE `queue_id` = '%s'" % (cfg.get(section, 'id')))
            count = cur.fetchone()[0]
            print queuename, 0, count, 'all'
    else:
        cur.execute("SELECT COUNT(*) FROM `ticket` WHERE `queue_id` = '%s'" % (cfg.get(section, 'id')))
        count = cur.fetchone()[0]
        print queuename, 0, count, 'all'
