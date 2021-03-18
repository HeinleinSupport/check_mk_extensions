#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)
from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
from cmk.gui.valuespec import (
    Alternative,
    CascadingDropdown,
    FixedValue,
    Integer,
    IPv4Address,
    ListOf,
    Tuple,
)

              
def _valuespec_agent_config_memcached():
    return CascadingDropdown(
        title = _("Memcached instances (Linux)"),
        help = _("If you activate this option, then the agent plugin <tt>memcached</tt> will be deployed. "
                 "For each configured or detected memcached instance there will be one new service with detailed "
                 "statistics of the current number of clients and processes and their various states."),
        choices = [
            ( "autodetect", _("Autodetect instances")
             ),
            ( "static", _("Specific list of instances"),
                ListOf(
                    Tuple(
                        elements = [
                            IPv4Address(
                                title = _("IPv4 Address"),
                                default_value = "127.0.0.1",
                            ),
                            Alternative(
                                elements = [
                                    FixedValue(None,
                                        title = _("Don't use custom port"),
                                        totext = _("Use default port"),
                                    ),
                                    Integer(
                                        title = _("TCP Port Number"),
                                        minvalue = 1,
                                        maxvalue = 65535,
                                        default_value = 11211,
                                    ),
                                ]
                            ),
                        ]
                    ),
                ),
            ),
            ( '_no_deploy', _("Do not deploy the memcached plugin") ),
        ]
    )

rulespec_registry.register(
     HostRulespec(
         group=RulespecGroupMonitoringAgentsAgentPlugins,
         name="agent_config:memcached",
         valuespec=_valuespec_agent_config_memcached,
     ))
