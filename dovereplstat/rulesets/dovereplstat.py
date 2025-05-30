#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    Tuple,
)

from cmk.gui.plugins.wato import (
    RulespecGroupCheckParametersApplications,
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
)

def _dovereplstat_parameters(title):
    return Tuple(title = title,
                 elements = [
                     Integer(title = "Warning at"),
                     Integer(title = "Critical at"),
                 ])

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="dovereplstat",
        group=RulespecGroupCheckParametersApplications,
        match_type = "dict",
        parameter_valuespec=lambda: Dictionary(
            help = _('This check uses the output of `doveadm replicator status`.'),
            elements = [
                ('sync_requests',
                 _dovereplstat_parameters(_('Levels for queued sync requests'))
                 ),
                ('high_requests',
                 _dovereplstat_parameters(_('Levels for queued high requests'))
                 ),
                ('low_requests',
                 _dovereplstat_parameters(_('Levels for queued low requests'))
                 ),
                ('failed_requests',
                 _dovereplstat_parameters(_('Levels for waiting failed requests'))
                 ),
                ('full_resync_requests',
                 _dovereplstat_parameters(_('Levels for queued full resync requests'))
                 ),
            ]
        ),
        title=lambda: _("Dovecot Replication Status"),
    ))
