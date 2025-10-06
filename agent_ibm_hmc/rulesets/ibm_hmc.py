#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2024 Heinlein Consulting GmbH
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
from cmk.gui.plugins.wato.special_agents.common import RulespecGroupDatasourceProgramsHardware
from cmk.gui.plugins.wato.utils import HostRulespec, rulespec_registry
from cmk.gui.watolib.rulespecs import Rulespec
from cmk.gui.valuespec import (
    Dictionary,
    TextAscii,
)

def _factory_default_special_agents_ibm_hmc():
    # No default, do not use setting if no rule matches
    return Rulespec.FACTORY_DEFAULT_UNUSED

def _valuespec_special_agents_ibm_hmc() -> Dictionary:
    return Dictionary(
        title = _(u'IBM HMC'),
        help = _(u'This rule selects the IBM HMC agent. You can configure your connection settings here.'),
        elements = [
            ( 'username',
              TextAscii(
                  title = _('User name'),
                  allow_empty = False,
              )
            ),
            ( 'ssh_id',
              TextAscii(
                  title = _('SSH key file'),
                  help = _('Enter the location of the SSH key file, usually ~/.ssh/id_rsa or similar'),
                  allow_empty = False,
              )
            ),
        ],
        optional_keys = [ 'ssh_id' ],
    )

rulespec_registry.register(
    HostRulespec(
        factory_default=_factory_default_special_agents_ibm_hmc(),
        group=RulespecGroupDatasourceProgramsHardware,
        name="special_agents:ibm_hmc",
        valuespec=_valuespec_special_agents_ibm_hmc,
    )
)
