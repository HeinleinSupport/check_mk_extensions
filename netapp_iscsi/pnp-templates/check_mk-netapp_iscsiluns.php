<?php
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2013             mk@mathias-kettner.de |
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
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

// new version of diskstat
if (isset($DS[2])) {

    $RRD = array();
    foreach ($NAME as $i => $n) {
        $RRD[$n] = "$RRDFILE[$i]:$DS[$i]:MAX";
        $WARN[$n] = $WARN[$i];
        $CRIT[$n] = $CRIT[$i];
        $MIN[$n]  = $MIN[$i];
        $MAX[$n]  = $MAX[$i];
    }

    // $parts = explode("_", $servicedesc);

    $opt[3] = "--vertical-label 'Size MB' -X0 --title \"$servicedesc size on $hostname\" ";

    $def[3] =  "HRULE:0#a0a0a0 ".
               "DEF:size=$RRD[size] ".
               "CDEF:size_mb=size,1048576,/ ".
               "AREA:size_mb#40c080:\"Size \" ".
               "GPRINT:size_mb:LAST:\"%8.1lf MB last\" ".
               "GPRINT:size_mb:AVERAGE:\"%6.1lf MB avg\" ".
               "GPRINT:size_mb:MAX:\"%6.1lf MB max\\n\" ";
    if (isset($RRD["size.avg"])) {
        $def[3] .=
               "DEF:size_avg=${RRD['size.avg']} ".
               "CDEF:size_avg_mb=size_avg,1048576,/ ".
               "LINE:size_avg_mb#202020 ";
    }

    $opt[1] = "--vertical-label 'Throughput (MB/s)' -X0  --title \"$servicedesc throughput on $hostname\" ";

    $def[1]  =
               "HRULE:0#a0a0a0 ".
    # read
               "DEF:read=$RRD[read] ".
               "CDEF:read_mb=read,1048576,/ ".
               "AREA:read_mb#40c080:\"Read \" ".
               "GPRINT:read_mb:LAST:\"%8.1lf MB/s last\" ".
               "GPRINT:read_mb:AVERAGE:\"%6.1lf MB/s avg\" ".
               "GPRINT:read_mb:MAX:\"%6.1lf MB/s max\\n\" ";

    # read average as line in the same graph
    if (isset($RRD["read.avg"])) {
        $def[1] .=
               "DEF:read_avg=${RRD['read.avg']} ".
               "CDEF:read_avg_mb=read_avg,1048576,/ ".
               "LINE:read_avg_mb#202020 ";
    }

    # write
    $def[1] .=
               "DEF:write=$RRD[write] ".
               "CDEF:write_mb=write,1048576,/ ".
               "CDEF:write_mb_neg=write_mb,-1,* ".
               "AREA:write_mb_neg#4080c0:\"Write  \"  ".
               "GPRINT:write_mb:LAST:\"%6.1lf MB/s last\" ".
               "GPRINT:write_mb:AVERAGE:\"%6.1lf MB/s avg\" ".
               "GPRINT:write_mb:MAX:\"%6.1lf MB/s max\\n\" ".
               "";

    # show levels for read
    if ($WARN['read']) {
        $def[1] .= "HRULE:$WARN[read]#ffd000:\"Warning for read at  " . sprintf("%6.1f", $WARN[1]) . " MB/s  \" ";
        $def[1] .= "HRULE:$CRIT[read]#ff0000:\"Critical for read at  " . sprintf("%6.1f", $CRIT[1]) . " MB/s\\n\" ";
    }

    # show levels for write
    if ($WARN['write']) {
        $def[1] .= "HRULE:-$WARN[write]#ffd000:\"Warning for write at " . sprintf("%6.1f", $WARN[2]) . " MB/s  \" ";
        $def[1] .= "HRULE:-$CRIT[write]#ff0000:\"Critical for write at " . sprintf("%6.1f", $CRIT[2]) . " MB/s\\n\" ";
    }

    $opt[2] = "--vertical-label 'IOps/s' -X0  --title \"$servicedesc Ops on $hostname\" ";

    $def[2]  =
               "HRULE:0#a0a0a0 ".
    # read
               "DEF:readops=$RRD[readops] ".
               "AREA:readops#40c080:\"Read Ops \" ".
               "GPRINT:readops:LAST:\"%8.1lf /s last\" ".
               "GPRINT:readops:AVERAGE:\"%6.1lf /s avg\" ".
               "GPRINT:readops:MAX:\"%6.1lf /s max\\n\" ";

    # read average as line in the same graph
    if (isset($RRD["readops.avg"])) {
        $def[2] .=
               "DEF:readops_avg=${RRD['readops.avg']} ".
               "LINE:readops_avg#202020 ";
    }

    # write
    $def[2] .=
               "DEF:writeops=$RRD[writeops] ".
               "CDEF:writeops_neg=writeops,-1,* ".
               "AREA:writeops_neg#4080c0:\"Write Ops  \"  ".
               "GPRINT:writeops:LAST:\"%6.1lf /s last\" ".
               "GPRINT:writeops:AVERAGE:\"%6.1lf /s avg\" ".
               "GPRINT:writeops:MAX:\"%6.1lf /s max\\n\" ".
               "";

    # show levels for read
    if ($WARN['readops']) {
        $def[2] .= "HRULE:$WARN[readops]#ffd000:\"Warning for read ops at  " . sprintf("%6.1f", $WARN['readops']) . " /s  \" ";
        $def[2] .= "HRULE:$CRIT[readops]#ff0000:\"Critical for read ops at  " . sprintf("%6.1f", $CRIT['readops']) . " /s\\n\" ";
    }

    # show levels for write
    if ($WARN['writeops']) {
        $def[2] .= "HRULE:-$WARN[writeops]#ffd000:\"Warning for write ops at " . sprintf("%6.1f", $WARN['writeops']) . " /s  \" ";
        $def[2] .= "HRULE:-$CRIT[writeops]#ff0000:\"Critical for write ops at " . sprintf("%6.1f", $CRIT['writeops']) . " /s\\n\" ";
    }

}

?>

