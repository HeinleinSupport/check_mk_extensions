#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Tuple,
    Integer,
    IPNetwork,
    ListOfStrings,
    MonitoringState,
    TextAscii,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithItem,
    HostRulespec,
    RulespecGroupCheckParametersApplications,
    RulespecGroupCheckParametersDiscovery,
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

def _valuespec_discovery_rbl_rules():
    return Dictionary(
        title=_('IP addresses and networks for RBL checks'),
        help=_('Configure the discovery of RBL checks.'),
        elements=[
            ('active',
             FixedValue(
                 True,
                 title=_('Discover IPs for RBL checks'),
                 totext=_('active'))),
            ('include',
             ListOf(
                 title=_("Include List"),
                 add_label=_("Add IP network or address"),
                 valuespec=IPNetwork(),
                 )),
            ('exclude',
             ListOf(
                 title=_("Exclude List"),
                 add_label=_("Add IP network or address"),
                 valuespec=IPNetwork(),
                 default_value=[
                     '10.0.0.0/8',
                     '127.0.0.0/8',
                     '172.16.0.0/12',
                     '192.168.0.0/16',
                     '::1/128',
                     'fe80::/10',
                     'fc00::/7',
                 ],)),
        ],
        optional_keys = ['include', 'exclude'],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupCheckParametersDiscovery,
        match_type="first",
        name="discovery_rbl_rules",
        valuespec=_valuespec_discovery_rbl_rules,
    ))
