#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Tuple,
    Integer,
    ListOfStrings,
    MonitoringState,
    TextAscii,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithItem,
    RulespecGroupCheckParametersApplications,
)

def _item_spec_netifaces_rbl():
    return TextAscii(
        title = _("Interface Address"),
        help = _("The IP address as returned by the netifaces agent plugin."),
        allow_empty = False
    )

def _parameter_valuespec_netifaces_rbl():
    return Dictionary(
        title = _("List of RBLs to check against"),
        help = _('The check <tt>netifaces_rbl</tt> monitors IP addresses of the host against the RBLs defined here.'),
        elements = [
            ( 'warn',
                ListOfStrings(
                    title = _("WARN"),
                    help = _('This list contains the RBLs that generate a WARNING state.'),
                ),
            ),
            ( 'crit',
                ListOfStrings(
                    title = _('CRIT'),
                    help = _('This list contains the RBLs that generate a CRITICAL state.'),
                    default_value = ['ix.dnsbl.manitu.net', 'bl.spamcop.net', 'zen.spamhaus.org'],
                ),
            ),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="netifaces_rbl",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_netifaces_rbl,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_netifaces_rbl,
        title=lambda: _("RBL"),
    ))
