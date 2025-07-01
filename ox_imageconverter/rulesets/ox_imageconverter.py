#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2023 Heinlein Consulting GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils.simple_levels import SimpleLevels
from cmk.gui.valuespec import (
    Dictionary,
    DropdownChoice,
    Filesize,
    Float,
    Integer,
    TextAscii,
    Tuple,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithoutItem,
    HostRulespec,
    RulespecGroupCheckParametersApplications,
)

# 'CacheHitRatio': { 'lower': (60, 40) },
# 'CacheKeyCount': { 'upper': (90000, 100000) },
# 'CacheSize': { 'lower': (10737418240, 0), 'upper': (32212254720, 42949672960) },
# 'MedianKeyProcessTimeMillis': { 'upper': (10, 100000) },

def _parameter_valuespec_ox_imageconverter_cache():
    return Dictionary(
        title = _('TITLE'),
        elements = [
            ( 'CacheHitRatio',
              Dictionary(
                  title = _('Cache Hit Ratio'),
                  elements = [
                      ('lower',
                       SimpleLevels(Float, title=_("Lower Levels"), default_levels = (60.0, 40.0), unit = "%")),
                  ],
                  optional_keys = [],
            )),
            ( 'CacheKeyCount',
              Dictionary(
                  title = _('Cache Key Count'),
                  elements = [
                      ('upper',
                       SimpleLevels(Integer, title=_("Upper Levels"), default_levels = (90000, 100000), unit = "keys")),
                  ],
                  optional_keys = [],
            )),
            ( 'CacheSize',
              Dictionary(
                  title = _('Cache Size'),
                  elements = [
                      ('lower',
                       SimpleLevels(Filesize, title=_("Lower Levels"), default_levels = (10737418240, 0) )),
                      ('upper',
                       SimpleLevels(Filesize, title=_("Upper Levels"), default_levels = (32212254720, 42949672960) )),
                  ],
                  optional_keys = [],
            )),
            ( 'MedianKeyProcessTimeMillis',
              Dictionary(
                  title = _('Median Key Processing Time'),
                  elements = [
                      ('upper',
                       SimpleLevels(Integer, title=_("Upper Levels"), default_levels = (10, 1000000), unit = "s")),
                  ],
                  optional_keys = [],
            )),
        ],
        ignored_keys = ["upsname", "model"],
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="ox_imageconverter_cache",
        group=RulespecGroupCheckParametersApplications,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_ox_imageconverter_cache,
        title=lambda: _("Open-Xchange ImageConverter Cache"),
    ))

try:
    from cmk.gui.plugins.wato import (
        HostRulespec,
        rulespec_registry,
    )
    from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
    from cmk.gui.valuespec import (
        DropdownChoice,
    )

    def _valuespec_agent_config_ox_imageconverter():
        return Alternative(
            title = _("Open-Xchange ImageConverter (Linux)"),
            help = _("This will deploy the agent plugin <tt>ox_imageconverter</tt> to check various Open-Xchange ImageConverter stats."),
            elements = [
                Dictionary(
                    title = _("Deploy the plugin for Open-Xchange ImageConverter"),
                    elements = [
                        (
                            "credentials",
                            Tuple(
                                title=_("Credentials to access the Database"),
                                elements=[
                                    TextInput(
                                        title=_("User ID"),
                                        default_value="monitoring",
                                    ),
                                    Password(title=_("Password")),
                                ],
                            ),
                        ),
                        (
                            "interval",
                            Age(
                                title=_("Run asynchronously"),
                                label=_("Interval for collecting data"),
                                default_value=300,
                            ),
                        ),
                    ],
                    optional_keys = ["interval"],
                ),
                FixedValue(
                    value = None,
                    title = _("Do not deploy plugin for Open-Xchange ImageConverter"),
                    totext = _("(disabled)"),
                ),
            ]
        )

    rulespec_registry.register(
         HostRulespec(
             group=RulespecGroupMonitoringAgentsAgentPlugins,
             name="agent_config:ox_imageconverter",
             valuespec=_valuespec_agent_config_ox_imageconverter,
         ))

except ModuleNotFoundError:
    # RAW edition
    pass
