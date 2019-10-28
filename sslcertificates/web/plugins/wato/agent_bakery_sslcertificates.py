#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_rule(
    "agents/" + _("Agent Plugins"),
    "agent_config:sslcertificates",
    Alternative(
        title = _("SSL Certificates"),
        help = _("This will deploy the agent plugin <tt>sslcertificates</tt> "
                 "for checking SSL certificate files. <b>Note:</b> If you want "
                 "to configure several directories to look into for SSL certificate "
                 "files, then simply create several rules. In this ruleset "
                 "<b>all</b> matching rules "
                 "are being executed, not only the first one. "),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy the SSL certificates plugin"),
                elements = [
                    ("interval", Age(
                        title = _("Run asynchronously"),
                        label = _("Interval for collecting data"),
                        default_value = 3600
                    )),
                   ( "directories",
                     ListOfStrings(
                        title = _("Directories or filename patterns to look into for SSL certificate files"),
                        help = _('Enter path patterns that will be searched for certificate files. Only works on Linux. On Windows the agent plugin looks into the cert store.'),
                        valuespec = TextAscii(
                            size = 80,
                            regex = "^/[^ \t]+$",
                            regex_error = _("Directory paths must begin with <tt>/</tt> and must not contain spaces."),
                       ),
                       allow_empty = False,

                     )
                   ),
                ],
                optional_keys = [ 'interval' ],
            ),
            FixedValue(None, title = _("Do not deploy the SSL certificates plugin"), totext = _("(disabled)") ),
        ]
    ),
)

# from cmk.gui.watolib.rulespecs import rulespec_registry
# from cmk.gui.plugins.wato.utils import HostRulespec
# from cmk.gui.cee.plugins.wato.agent_bakery import RulespecGroupMonitoringAgentsAgentPlugins

# def _valuespec_agent_config_sslcertificates():
#     return Alternative(
#         title = _("SSL Certificates"),
#         help = _("This will deploy the agent plugin <tt>sslcertificates</tt> "
#                  "for checking SSL certificate files. <b>Note:</b> If you want "
#                  "to configure several directories to look into for SSL certificate "
#                  "files, then simply create several rules. In this ruleset "
#                  "<b>all</b> matching rules "
#                  "are being executed, not only the first one. "),
#         style = "dropdown",
#         elements = [
#             Dictionary(
#                 title = _("Deploy the SSL certificates plugin"),
#                 elements = [
#                     ("interval", Age(
#                         title = _("Run asynchronously"),
#                         label = _("Interval for collecting data"),
#                         default_value = 3600
#                     )),
#                     ( "directories", ListOfStrings(
#                         title = _("Directories or filename patterns to look into for SSL certificate files"),
#                         help = _('Enter path patterns that will be searched for certificate files. Only works on Linux. On Windows the agent plugin looks into the cert store.'),
#                         valuespec = TextAscii(
#                             size = 80,
#                             regex = "^/[^ \t]+$",
#                             regex_error = _("Directory paths must begin with <tt>/</tt> and must not contain spaces."),
#                        ),
#                        allow_empty = False,
#                      )
#                    ),
#                 ],
#                 optional_keys = ['interval'],
#             ),
#             FixedValue(None, title = _("Do not deploy the SSL certificates plugin"), totext = _("(disabled)") ),
#         ]
#     )

# rulespec_registry.register(
#     HostRulespec(
#         group=RulespecGroupMonitoringAgentsAgentPlugins,
#         name="agent_config:sslcertificates",
#         valuespec=_valuespec_agent_config_sslcertificates,
#     ))
