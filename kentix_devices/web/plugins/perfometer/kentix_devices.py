#!/usr/bin/env python

def perfometer_motion(row, check_command, perf_data):
    motion = float(perf_data[0][1])
    return "%3.1f% %" % motion, perfometer_linear(motion, '#90D4A9')

perfometers['check_mk-kentix_devices.motion'] = perfometer_motion
