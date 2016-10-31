#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def dovereplstat_parameters(title):
    return Tuple(title = title,
                 elements = [
                     Integer(title = "Warning at"),
                     Integer(title = "Critical at"),
                 ])

register_check_parameters(
    subgroup_applications,
    "dovereplstat",
    _("Dovecot Replication Status"),
    Dictionary(
        help = _('This check uses the output of `doveadm replicator status`.'),
        elements = [
            ('sync_requests',
             dovereplstat_parameters(_('Levels for queued sync requests'))
             ),
            ('high_requests',
             dovereplstat_parameters(_('Levels for queued high requests'))
             ),
            ('low_requests',
             dovereplstat_parameters(_('Levels for queued low requests'))
             ),
            ('failed_requests',
             dovereplstat_parameters(_('Levels for waiting failed requests'))
             ),
            ('full_resync_requests',
             dovereplstat_parameters(_('Levels for queued full resync requests'))
             ),
        ]
    ),
    False,
    match_type = "dict",
)

