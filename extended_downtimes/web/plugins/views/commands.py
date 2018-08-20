#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2014             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.



#.
#   .--Downtimes-----------------------------------------------------------.
#   |         ____                      _   _                              |
#   |        |  _ \  _____      ___ __ | |_(_)_ __ ___   ___  ___          |
#   |        | | | |/ _ \ \ /\ / / '_ \| __| | '_ ` _ \ / _ \/ __|         |
#   |        | |_| | (_) \ V  V /| | | | |_| | | | | | |  __/\__ \         |
#   |        |____/ \___/ \_/\_/ |_| |_|\__|_|_| |_| |_|\___||___/         |
#   |                                                                      |
#   '----------------------------------------------------------------------'

def command_downtime(cmdtag, spec, row):
    down_from = int(time.time())
    down_to = None

    if has_recurring_downtimes() and html.get_checkbox("_down_do_recur"):
        recurring_type = int(html.var("_down_recurring"))
        title_start = _("schedule a periodic downtime every %s") % wato.recurring_downtimes_types[recurring_type]
    else:
        title_start = _("schedule an immediate downtime")

    if html.var("_down_2h"):
        down_to = down_from + 7200
        title = _("<b>%s of 2 hours length</b> on") % title_start

    elif html.var("_down_4h"):
        down_to = down_from + 14400
        title = _("<b>%s of 4 hours length</b> on") % title_start

    elif html.var("_down_today"):
        br = time.localtime(down_from)
        down_to = time.mktime((br.tm_year, br.tm_mon, br.tm_mday, 23, 59, 59, 0, 0, br.tm_isdst)) + 1
        title = _("<b>%s until 24:00:00</b> on") % title_start

    elif html.var("_down_today_plus"):
        br = time.localtime(down_from)
        down_to = time.mktime((br.tm_year, br.tm_mon, br.tm_mday + 1, 10, 0, 0, 0, 0, br.tm_isdst))
        title = _("<b>%s until 10:00 tomorrow</b> on") % title_start

    elif html.var("_down_week"):
        br = time.localtime(down_from)
        wday = br.tm_wday
        days_plus = 6 - wday
        down_to = time.mktime((br.tm_year, br.tm_mon, br.tm_mday, 23, 59, 59, 0, 0, br.tm_isdst)) + 1
        down_to += days_plus * 24 * 3600
        title = _("<b>%s until sunday night</b> on") % title_start

    elif html.var("_down_week_plus"):
        br = time.localtime(down_from)
        wday = br.tm_wday
        days_plus = 7 - wday
        down_to = time.mktime((br.tm_year, br.tm_mon, br.tm_mday + days_plus, 10, 0, 0, 0, 0, br.tm_isdst))
        title = _("<b>%s until monday morning 10:00</b> on") % title_start

    elif html.var("_down_month"):
        br = time.localtime(down_from)
        new_month = br.tm_mon + 1
        if new_month == 13:
            new_year = br.tm_year + 1
            new_month = 1
        else:
            new_year = br.tm_year
        down_to = time.mktime((new_year, new_month, 1, 0, 0, 0, 0, 0, br.tm_isdst))
        title = _("<b>%s until end of month</b> on") % title_start

    elif html.var("_down_month_plus"):
        br = time.localtime(down_from)
        tmp = time.localtime(time.mktime((br.tm_year, br.tm_mon + 1, 1, 9, 0, 0, 0, 0, br.tm_isdst)))
        days_plus = 0
        if tmp.tm_wday == 6:
            days_plus = 1
        if tmp.tm_wday == 5:
            days_plus = 2
        down_to = time.mktime((tmp.tm_year, tmp.tm_mon, tmp.tm_mday + days_plus, 10, 0, 0, 0, 0, tmp.tm_isdst))
        title = _("<b>%s until start of next month (%s)</b> on") % (title_start, time.strftime('%Y-%m-%d %H:%M', time.localtime(down_to)))

    elif html.var("_down_year"):
        br = time.localtime(down_from)
        down_to = time.mktime((br.tm_year, 12, 31, 23, 59, 59, 0, 0, br.tm_isdst)) + 1
        title = _("<b>%s until end of %d</b> on") % (title_start, br.tm_year)

    elif html.var("_down_year_plus"):
        br = time.localtime(down_from)
        tmp = time.localtime(time.mktime((br.tm_year + 1, 1, 2, 9, 0, 0, 0, 0, br.tm_isdst)))
        days_plus = 0
        if tmp.tm_wday == 6:
            days_plus = 1
        if tmp.tm_wday == 5:
            days_plus = 2
        down_to = time.mktime((tmp.tm_year, tmp.tm_mon, tmp.tm_mday + days_plus, 10, 0, 0, 0, 0, tmp.tm_isdst))
        title = _("<b>%s until start of next year (%s) </b> on") % (title_start, time.strftime('%Y-%m-%d %H:%M', time.localtime(down_to)))

    elif html.var("_down_from_now"):
        try:
            minutes = int(html.var("_down_minutes"))
        except:
            minutes = 0

        if minutes <= 0:
            raise MKUserError("_down_minutes", _("Please enter a positive number of minutes."))

        down_to = time.time() + minutes * 60
        title = _("<b>%s for the next %d minutes</b> on" % (title_start, minutes))

    elif html.var("_down_adhoc"):
        minutes = config.adhoc_downtime.get("duration",0)
        down_to = time.time() + minutes * 60
        title = _("<b>%s for the next %d minutes</b> on" % (title_start, minutes))

    elif html.var("_down_custom"):
        down_from = html.get_datetime_input("_down_from")
        down_to   = html.get_datetime_input("_down_to")
        if down_to < time.time():
            raise MKUserError("_down_to", _("You cannot set a downtime that ends in the past. "
                         "This incident will be reported."))

        if down_to < down_from:
            raise MKUserError("_down_to", _("Your end date is before your start date."))

        title = _("<b>schedule a downtime from %s to %s</b> on ") % (
            time.asctime(time.localtime(down_from)),
            time.asctime(time.localtime(down_to)))

    elif html.var("_down_remove"):
        if html.var("_on_hosts"):
            raise MKUserError("_on_hosts", _("The checkbox for setting host downtimes does not work when removing downtimes."))

        downtime_ids = []
        if cmdtag == "HOST":
            prefix = "host_"
        else:
            prefix = "service_"
        for id in row[prefix + "downtimes"]:
            if id != "":
                downtime_ids.append(int(id))

        commands = []
        for dtid in downtime_ids:
            commands.append("DEL_%s_DOWNTIME;%d\n" % (cmdtag, dtid))
        title = _("<b>remove all scheduled downtimes</b> of ")
        return commands, title

    if down_to:
        if html.var("_down_adhoc"):
            comment = config.adhoc_downtime.get("comment","")
        else:
            comment = html.get_unicode_input("_down_comment")
        if not comment:
            raise MKUserError("_down_comment", _("You need to supply a comment for your downtime."))
        if html.var("_down_flexible"):
            fixed = 0
            duration = html.get_time_input("_down_duration", _("the duration"))
        else:
            fixed = 1
            duration = 0

        if html.get_checkbox("_down_do_recur"):
            fixed_and_recurring = recurring_type * 2 + fixed
        else:
            fixed_and_recurring = fixed

        def make_command(spec, cmdtag):
            return ("SCHEDULE_" + cmdtag + "_DOWNTIME;%s;" % spec ) \
                   + ("%d;%d;%d;0;%d;%s;" % (down_from, down_to, fixed_and_recurring, duration, config.user.id)) \
                   + lqencode(comment)

        if "aggr_tree" in row: # BI mode
            commands = []
            for site, host, service in bi.find_all_leaves(row["aggr_tree"]):
                if service:
                    spec = "%s;%s" % (host, service)
                    cmdtag = "SVC"
                else:
                    spec = host
                    cmdtag = "HOST"
                commands.append((site, make_command(spec, cmdtag)))
        else:
            if html.var("_include_childs"): # only for hosts
                specs = [ spec ] + get_child_hosts(row["site"], [spec], recurse = not not html.var("_include_childs_recurse"))
            elif html.var("_on_hosts"): # set on hosts instead of services
                specs = [ spec.split(";")[0] ]
                title += " the hosts of"
                cmdtag = "HOST"
            else:
                specs = [ spec ]

            commands = [ make_command(spec, cmdtag) for spec in  specs ]

        return commands, title

def paint_downtime_buttons(what):
    html.write(_('Downtime Comment')+": ")
    html.text_input("_down_comment", "", size=60, submit="")
    html.write("<hr>")
    html.button("_down_from_now", _("From now for"))
    html.write("&nbsp;")
    html.number_input("_down_minutes", 60, size=4, submit="_down_from_now")
    html.write("&nbsp; " + _("minutes"))
    html.write("<hr>")
    html.button("_down_2h", _("2 hours"))
    html.button("_down_4h", _("4 hours"))
    html.button("_down_today", _("Today"))
    html.button("_down_today_plus", _("10:00 tomorrow"))
    html.button("_down_week", _("This week"))
    html.button("_down_week_plus", _("10:00 next monday"))
    html.button("_down_month", _("This month"))
    html.button("_down_month_plus", _("Start of next month"))
    html.button("_down_year", _("This year"))
    html.button("_down_year_plus", _("Start of next year"))
    if what != "aggr":
        html.write(" &nbsp; - &nbsp;")
        html.button("_down_remove", _("Remove all"))
    html.write("<hr>")
    if config.adhoc_downtime and config.adhoc_downtime.get("duration"):
        adhoc_duration = config.adhoc_downtime.get("duration")
        adhoc_comment  = config.adhoc_downtime.get("comment", "")
        html.button("_down_adhoc", _("Adhoc for %d minutes") % adhoc_duration)
        html.write("&nbsp;")
        html.write(_('with comment')+": ")
        html.write(adhoc_comment)
        html.write("<hr>")

    html.button("_down_custom", _("Custom time range"))
    html.datetime_input("_down_from", time.time(), submit="_down_custom")
    html.write("&nbsp; "+_('to')+" &nbsp;")
    html.datetime_input("_down_to", time.time() + 7200, submit="_down_custom")
    html.write("<hr>")
    html.checkbox("_down_flexible", False, label=_('flexible with duration')+" ")
    html.time_input("_down_duration", 2, 0)
    html.write(" "+_('(HH:MM)'))
    if what == "host":
        html.write("<hr>")
        html.checkbox("_include_childs", False, label=_('Also set downtime on child hosts'))
        html.write("  ")
        html.checkbox("_include_childs_recurse", False, label=_('Do this recursively'))
    elif what == "service":
        html.write("<hr>")
        html.checkbox("_on_hosts", False, label=_('Schedule downtimes on the affected '
                                                  '<b>hosts</b> instead of on the individual '
                                                  'services'))

    if has_recurring_downtimes():
        html.write("<hr>")
        html.checkbox("_down_do_recur", False,
                      label=_("Repeat this downtime on a regular base every"))
        html.write(" ")
        recurring_selections = [ (str(k), v) for (k,v) in
                                 sorted(wato.recurring_downtimes_types.items())]
        html.select("_down_recurring", recurring_selections, "3")
        html.write(_("(This only works when using CMC)"))

for mc in multisite_commands[:]:
    if mc['permission'] == 'action.downtimes':
        if mc['tables'] == [ "host" ]:
            multisite_commands.remove(mc)
            multisite_commands.append({
                "tables"      : [ "host" ],
                "permission"  : "action.downtimes",
                "title"       : _("Schedule downtimes"),
                "render"      : lambda: paint_downtime_buttons("host"),
                "action"      : command_downtime,
                "group"       : "downtimes",
            })
        if mc['tables'] == [ "service" ]:
            multisite_commands.remove(mc)
            multisite_commands.append({
                "tables"      : [ "service" ],
                "permission"  : "action.downtimes",
                "title"       : _("Schedule downtimes"),
                "render"      : lambda: paint_downtime_buttons("service"),
                "action"      : command_downtime,
                "group"       : "downtimes",
            })
        if mc['tables'] == [ "aggr" ]:
            multisite_commands.remove(mc)
            multisite_commands.append({
                "tables"      : [ "aggr" ],
                "permission"  : "action.downtimes",
                "title"       : _("Schedule downtimes"),
                "render"      : lambda: paint_downtime_buttons("aggr"),
                "action"      : command_downtime,
                "group"       : "downtimes",
            })

