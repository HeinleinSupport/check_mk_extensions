#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.rulesets.v1 import (
    Help,
    Label,
    Title,
)
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    InputHint,
    LevelDirection,
    LevelsType,
    List,
    migrate_to_lower_float_levels,
    SimpleLevels,
    String,
    TimeMagnitude,
    TimeSpan,
    validators,
)
from cmk.rulesets.v1.rule_specs import (
    AgentConfig,
    CheckParameters,
    DiscoveryParameters,
    HostAndItemCondition,
    Topic,
)

_netifaces_condition = HostAndItemCondition(
    item_title=Title("Interface Address"),
    item_form=String(
        help_text=Help("The IP address as returned by the netifaces agent plugin."),
    )
)

def _parameter_valuespec_netifaces_rbl():
    return Dictionary(
        help_text = Help('The check <tt>netifaces_rbl</tt> monitors IP addresses of the host against the RBLs defined here.'),
        elements = {
            'warn': DictElement(
                parameter_form=List(
                    title=Title("WARN"),
                    help_text=Help("This list contains the RBLs that generate a WARNING state."),
                    element_template=String(),
                )
            ),
            'crit': DictElement(
                parameter_form=List(
                    title=Title("CRIT"),
                    help_text=Help("This list contains the RBLs that generate a CRITICAL state."),
                    element_template=String(),
                    editable_order=False,
                    # default_value = ['ix.dnsbl.manitu.net', 'bl.spamcop.net', 'zen.spamhaus.org'],
                )                
            ),
        },
    )

rule_spec_netifaces_rbl = CheckParameters(
    name="netifaces_rbl",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_netifaces_rbl,
    title=Title("List of RBLs to check against"),
    condition=_netifaces_condition,
)

def _valuespec_discovery_rbl_rules():
    return Dictionary(
        elements={
            'active': DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    title=Title("Discover IPs for RBL checks"),
                    label=Label("enable"),
                ),
            ),
            'include': DictElement(
                parameter_form=List(
                    title=Title("Include List"),
                    add_element_label=Label("Add IP network or address"),
                    element_template=String(),
                ),
            ),
            'exclude': DictElement(
                parameter_form=List(
                    title=Title("Exclude List"),
                    add_element_label=Label("Add IP network or address"),
                    element_template=String(),
        #          default_value=[
        #              '10.0.0.0/8',
        #              '127.0.0.0/8',
        #              '172.16.0.0/12',
        #              '192.168.0.0/16',
        #              '::1/128',
        #              'fe80::/10',
        #              'fc00::/7',
        #          ]
                ),
            ),
        },
    )

rule_spec_discovery_rbl_rules = DiscoveryParameters(
    name="discovery_rbl_rules",
    parameter_form=_valuespec_discovery_rbl_rules,
    topic=Topic.GENERAL,
    title=Title("IP addresses and networks for RBL checks"),
    help_text=Help("Configure the discovery of RBL checks."),
)
# rulespec_registry.register(
#     HostRulespec(
#         group=RulespecGroupCheckParametersDiscovery,
#         match_type="first",
#         name="discovery_rbl_rules",
#         valuespec=_valuespec_discovery_rbl_rules,
#     ))

def _parameter_valuespec_netifaces_senderscore():
    return Dictionary(
        help_text = Help('The check <tt>netifaces_senderscore</tt> monitors IP addresses of the host against the score from senderscore.org.'),
        elements = {
            'score_levels': DictElement(
                required=True,
                parameter_form=SimpleLevels(
                    form_spec_template=Integer(
                        unit_symbol="%",
                    ),
                    title=Title("Sender Score levels"),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    prefill_fixed_levels=DefaultValue((80, 70)),
                    level_direction=LevelDirection.LOWER,
                ),
            ),
        },
    )

rule_spec_netifaces_senderscore = CheckParameters(
    name="netifaces_senderscore",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_netifaces_senderscore,
    title=Title("Sender Score"),
    condition=_netifaces_condition,
)

# def _valuespec_discovery_senderscore_rules():
#     return Dictionary(
#         title=_('IP addresses and networks for SenderScore checks'),
#         help=_('Configure the discovery of SenderScore checks.'),
#         elements=[
#             ('active',
#              FixedValue(
#                  True,
#                  title=_('Discover IPs for SenderScore checks'),
#                  totext=_('active'))),
#             ('include',
#              ListOf(
#                  title=_("Include List"),
#                  add_label=_("Add IP network or address"),
#                  valuespec=IPNetwork(),
#                  )),
#             ('exclude',
#              ListOf(
#                  title=_("Exclude List"),
#                  add_label=_("Add IP network or address"),
#                  valuespec=IPNetwork(),
#                  default_value=[
#                      '10.0.0.0/8',
#                      '127.0.0.0/8',
#                      '172.16.0.0/12',
#                      '192.168.0.0/16',
#                      '::1/128',
#                      'fe80::/10',
#                      'fc00::/7',
#                  ],)),
#         ],
#         optional_keys = ['include', 'exclude'],
#     )

# rulespec_registry.register(
#     HostRulespec(
#         group=RulespecGroupCheckParametersDiscovery,
#         match_type="first",
#         name="discovery_senderscore_rules",
#         valuespec=_valuespec_discovery_senderscore_rules,
#     ))
