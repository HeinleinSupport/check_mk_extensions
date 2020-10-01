#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
    CheckParameterRulespecWithItem,
    RulespecGroupCheckParametersApplications,
)
from cmk.gui.valuespec import (
    DropdownChoice,
    Filesize,
    Optional,
    TextAscii,
    Tuple,
)
from cmk.gui.cee.plugins.wato.agent_bakery import RulespecGroupMonitoringAgentsAgentPlugins

def _valuespec_agent_config_msexch_database_size():
    return DropdownChoice(
        title = _("MS Exchange Database Size (Windows)"),
        help = _("This will deploy the agent plugin <tt>msexch_database_size.ps1</tt> for monitoring the size of MS Exchange databases."),
        choices = [
            ( True, _("Deploy plugin for MS Exchange database size") ),
            ( None, _("Do not deploy plugin for MS Exchange database size") ),
        ]
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:msexch_database_size",
        valuespec=_valuespec_agent_config_msexch_database_size,
    ))


def _item_spec_msexch_database_size():
    return TextAscii(
        title=_("Name of the database"),
    )


def _parameter_valuespec_msexch_database_size():
    return Optional(
        Tuple(elements=[
            Filesize(title=_("warning at")),
            Filesize(title=_("critical at")),
        ],),
        help=_("The check will trigger a warning or critical state if the size of the "
               "database exceeds these levels."),
        title=_("Impose limits on the size of the database"),
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="msexch_database_size",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_msexch_database_size,
        parameter_valuespec=_parameter_valuespec_msexch_database_size,
        title=lambda: _("Size of MS Exchange databases"),
    ))
