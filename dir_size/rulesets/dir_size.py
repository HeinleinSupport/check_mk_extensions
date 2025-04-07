#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Filesize,
    TextAscii,
    Transform,
    Tuple,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithItem,
    RulespecGroupCheckParametersStorage,
)

def transform_dir_size_rules(p):
    if 'unit' in p:
        dir_size_factor = {
            'B': 1,
            'KB': 1024,
            'MB': 1048576,
            'GB': 1073741824,
            'TB': 1099511627776,
        }
        warn = p.get('warn')
        crit = p.get('crit')

        factor = p.get(p['unit'])
        if warn and factor:
            warn *= factor
        if crit and factor:
            crit *= factor
        return { 'levels_upper': (warn, crit) }
    return p

def _parameter_valuespec_dir_size():
    return Transform(
        Dictionary(
            title = _("Limits"),
            help = _("Size of all files and subdirectories"),
            elements = [
                ( 'levels_upper',
                  Tuple(
                      title = _('Upper levels for the total size'),
                      elements = [
                          Filesize(title = _("Warning at")),
                          Filesize(title = _("Critical at")),
                      ],
                  )),
            ],
            required_keys = [ "levels_upper" ],
        ),
        forth = transform_dir_size_rules,
    )

def _item_spec_dir_size():
    return TextAscii(
        title = _("Directory"),
        allow_empty = False,
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="dir_size",
        group=RulespecGroupCheckParametersStorage,
        item_spec=_item_spec_dir_size,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_dir_size,
        title=lambda: _("Directory Size Limits"),
    ))
