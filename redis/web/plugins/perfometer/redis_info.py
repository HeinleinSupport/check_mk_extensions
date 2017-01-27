#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Check_MK Redis Info Plugin
#
# Copyright 2016, Clemens Steinkogler <c.steinkogler[at]cashpoint.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


def float_or_int(value):
    if isinstance(value, int):
        return saveint(value)

    if isinstance(value, float):
        return savefloat(value)

    if isinstance(value, basestring):
        value_int = saveint(value)
        value_float = savefloat(value)

        if str(value_int) == str(value):
            return value_int

        if str(value_float) == str(value):
            return value_float
    # endif
# enddef


def perfometer_redis_info(row, command, perf_data):
    # debug_file = file("/tmp/redis_info_perfometer.log", "a")
    # debug_file.write(str(perf_data))
    # debug_file.close()
    # return u"%s" % str(perf_data[0][1]), perfometer_linear(int(perf_data[0][1]), 'silver')
    half = float_or_int(perf_data[0][1]) / 2
    if half <= 1:
        half = 2
    base = 2
    return u"%s" % str(perf_data[0][1]), perfometer_logarithmic(float_or_int(perf_data[0][1]), half, base, 'silver')

perfometers['check_mk-redis_info'] = perfometer_redis_info
