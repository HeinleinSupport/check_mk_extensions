#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2024 Matthias Henze - License: GNU General Public License v2
# Contact: mahescho@gmail.com

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
        Dictionary,
        Integer,
        Tuple,
        )
from cmk.gui.plugins.wato import (
        CheckParameterRulespecWithItem,
        rulespec_registry,
        RulespecGroupCheckParametersEnvironment,
        )

def _parameter_valuespec_wireguard():
    return Dictionary (
            title = _("Wireguard"),
            elements = [
                ("timeout", Tuple (
                    title = _("Timeout"),
                    elements = [
                        Integer(title = _("Warning above"), default_value = 300),
                        Integer(title = _("Critical above"), default_value = 3000),
                    ],
                    )),
                ],
            )

rulespec_registry.register (
        CheckParameterRulespecWithItem(
            check_group_name = "wireguard_data",
            group = RulespecGroupCheckParametersEnvironment,
            match_type = "dict",
            parameter_valuespec = _parameter_valuespec_wireguard,
            title = lambda: _("Wireguard"),
            )
        )
