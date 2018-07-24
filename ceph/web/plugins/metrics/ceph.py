#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2017 Heinlein Support GmbH
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

metric_info['num_objects'] = {
    'title' : _('Number of Objects'),
    'unit'  : 'count',
    'color' : '51/a',
}

metric_info['num_pgs'] = {
    'title' : _('Number of Placement Groups'),
    'unit'  : 'count',
    'color' : '52/a',
}

_ceph_pgstates = ['pgstate_active_clean',
                  'pgstate_active_clean_inconsistent',
                  'pgstate_active_clean_remapped',
                  'pgstate_active_clean_scrubbing',
                  'pgstate_active_clean_scrubbing_deep',
                  'pgstate_active_recovering',
                  'pgstate_active_recovering_degraded',
                  'pgstate_active_recovering_degraded_inconsistent',
                  'pgstate_active_recovery_wait',
                  'pgstate_active_recovery_wait_degraded',
                  'pgstate_active_recovery_wait_degraded_inconsistent',
                  'pgstate_active_recovery_wait_degraded_remapped',
                  'pgstate_active_recovery_wait_remapped',
                  'pgstate_active_recovery_wait_undersized_degraded',
                  'pgstate_active_recovery_wait_undersized_degraded_remapped',
                  'pgstate_active_remapped_inconsistent_backfill_wait',
                  'pgstate_active_remapped_inconsistent_backfilling',
                  'pgstate_active_undersized',
                  'pgstate_active_undersized_degraded',
                  'pgstate_active_undersized_degraded_inconsistent',
                  'pgstate_active_undersized_remapped',
                  'pgstate_active_undersized_degraded_remapped_backfilling',
                  'pgstate_active_undersized_degraded_remapped_backfill_wait',
                  'pgstate_active_undersized_degraded_remapped_inconsistent_backfilling',
                  'pgstate_active_undersized_degraded_remapped_inconsistent_backfill_wait',
                  'pgstate_active_remapped_backfill_wait',
                  'pgstate_active_remapped_backfilling',
                  'pgstate_peering',
                  'pgstate_remapped_peering',
                  'pgstate_stale_active_undersized_degraded',
                  'pgstate_undersized_degraded_peered',
                 ]

_ceph_num_pgstates = len(_ceph_pgstates)
_ceph_pg_metrics = [ ( 'num_pgs', 'line', _('Total') ) ]
_ceph_pg_metrics_optional = []

for idx, _ceph_pgstate in enumerate(_ceph_pgstates):
    _ceph_title = " + ".join(map(lambda x: x.capitalize(), _ceph_pgstate.split('_')[1:]))
    metric_info[_ceph_pgstate] = {
        'title' : _('PGs %s' % _ceph_title),
        'unit'  : 'count',
        'color' : indexed_color(idx+1, _ceph_num_pgstates),
    }
    _ceph_pg_metrics.append( ( _ceph_pgstate, 'stack', _ceph_title ) )
    _ceph_pg_metrics_optional.append( _ceph_pgstate )

metric_info['pgstates'] = {
    'title' : _('Placement Groups'),
    'unit'  : 'count',
    'color' : '53/a',
}

check_metrics["check_mk-cephstatus"] = {
    "Status"  : { "name"  : "fs_used", "scale" : MB },
    "fs_size" : { "scale" : MB },
    "growth"  : { "name"  : "fs_growth", "scale" : MB / 86400.0 },
    "trend"   : { "name"  : "fs_trend", "scale" : MB / 86400.0 },
}

check_metrics["check_mk-cephstatus"]['num_objects'] = {}
check_metrics["check_mk-cephstatus"]['num_pgs'] = {}
# check_metrics["check_mk-cephstatus"]['pgstates'] = { 'name': 'pgstates' }
check_metrics["check_mk-cephstatus"]['~pgstate_.*'] = {}

check_metrics["check_mk-cephdf"] = {
    "~(?!inodes_used|fs_size|growth|trend|fs_provisioning|"
      "uncommitted|overprovisioned|num_|disk_).*$"   : { "name"  : "fs_used", "scale" : MB },
    "fs_size" : { "scale" : MB },
    "growth"  : { "name"  : "fs_growth", "scale" : MB / 86400.0 },
    "trend"   : { "name"  : "fs_trend", "scale" : MB / 86400.0 },
}
check_metrics["check_mk-cephdf"]["num_objects"] = {}
check_metrics["check_mk-cephdf"]["disk_read_ios"] = {}
check_metrics["check_mk-cephdf"]["disk_write_ios"] = {}
check_metrics["check_mk-cephdf"]["disk_read_throughput"] = {}
check_metrics["check_mk-cephdf"]["disk_write_throughput"] = {}

metric_info["apply_latency"] = {
    'title' : _('Apply Latency'),
    'unit'  : 's',
    'color' : '22/a',
}

metric_info["commit_latency"] = {
    'title' : _('Commit Latency'),
    'unit'  : 's',
    'color' : '24/a',
}

check_metrics["check_mk-cephosd"] = df_translation
check_metrics["check_mk-cephosd"]["apply_latency"] = {}
check_metrics["check_mk-cephosd"]["commit_latency"] = {}

graph_info.append({
    'title'  : _('OSD Latency'),
    'metrics': [ ('apply_latency', 'line' ), ('commit_latency', 'line' ) ],
})

graph_info.append({
    'title'  : _('Placement Groups'),
    'metrics': _ceph_pg_metrics,
    'optional_metrics': _ceph_pg_metrics_optional,
    'range'  : (0, 'num_pgs:max'),
})
