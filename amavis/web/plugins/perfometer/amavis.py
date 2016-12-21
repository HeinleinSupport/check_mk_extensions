#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def perfometer_amavis(row, check_command, perf_data):
    for pd in perf_data:
        if pd[0] == u'amavis_child_busy':
            busy = float(pd[1])
            warn = float(pd[3])
            crit = float(pd[4])
            if busy <= warn:
                color = '#90ee90'
            elif busy <= crit:
                color = '#ffa500'
            else:
                color = '#ff6347'
            return '%d%%' % busy, perfometer_linear(busy, color)

perfometers["check_mk-amavis"] = perfometer_amavis
