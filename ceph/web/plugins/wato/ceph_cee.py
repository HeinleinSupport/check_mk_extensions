#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2020 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

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

try:
    from cmk.gui.i18n import _
    from cmk.gui.plugins.wato import (
        HostRulespec,
        rulespec_registry,
    )
    from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
    from cmk.gui.valuespec import (
        Alternative,
        Dictionary,
        Filename,
        TextInput,
        Transform,
    )

    def _transform_agent_config_ceph(p):
        if isinstance(p, bool):
            if p:
                return {'interval': 58}
            return None
        return p

    def _valuespec_agent_config_ceph():
        return Transform(
            Alternative(
                title = _("Ceph Status (Linux)"),
                help = _("This will deploy the agent plugin <tt>ceph</tt> for monitoring the status of Ceph. This plugin will be run asynchronously in the background."),
                style = "dropdown",
                elements = [
                    Dictionary(
                        title = _("Deploy plugin for Ceph"),
                        elements = [
                            ( "interval",
                              Age(
                                  title = _("Run asynchronously"),
                                  label = _("Interval for collecting data from Ceph"),
                                  default_value = 58,
                                  )),
                            ( "config",
                              Filename(
                                  title = _("Path to ceph.conf"),
                                  default_value = "/etc/ceph/ceph.conf",
                                  )),
                            ( "client",
                              TextInput(
                                  title = _("Client name"),
                                  default_value = "client.admin",
                                  )),
                        ],
                        optional_keys = ['config', 'client'],
                    ),
                    FixedValue( None, title = _("Do not deploy plugin for Ceph"), totext = _('(disabled)') ),
                ],
            ),
            forth=_transform_agent_config_ceph,
        )

    rulespec_registry.register(
         HostRulespec(
             group=RulespecGroupMonitoringAgentsAgentPlugins,
             name="agent_config:ceph",
             valuespec=_valuespec_agent_config_ceph,
         ))

except ModuleNotFoundError:
    # RAW edition
    pass
