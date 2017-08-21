#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_check_parameters(
    subgroup_applications,
    "ox_filestore",
    _("Open-Xchange Filestores Levels"),
    Dictionary(
        title = _('Levels for Open-Xchange file stores'),
        elements = [
            ( 'reserved', Tuple(
                title = _('Reserved'),
                elements = [
                    Integer(title = _("Warning at"), unit = _("%"), default_value = 80),
                    Integer(title = _("Critical at"), unit = _("%"), default_value = 90),
                ])),
            ( 'used', Tuple(
                title = _('Used'),
                elements = [
                    Integer(title = _("Warning at"), unit = _("%"), default_value = 80),
                    Integer(title = _("Critical at"), unit = _("%"), default_value = 90),
                ])),
            ( 'ent', Tuple(
                title = _('Entities'),
                elements = [
                    Integer(title = _("Warning at"), unit = _("%"), default_value = 80),
                    Integer(title = _("Critical at"), unit = _("%"), default_value = 90),
                ])),
          ]
    ),
    TextAscii(
        title = _("Filestore URL"),
        help = _('OX filestore URL starting with "file:/". You can make the rule apply only to certain filestores of the specified hosts. Do this by specifying explicit items to match here. <b>Hint:</b> make sure to enter the filestore URL only, not the full Service description. <b>Note:</b> the match is done on the <u>beginning</u> of the item in question. Regular expressions are interpreted, so appending a $ will force an exact match.')
    ),
    match_type = 'dict',
)

register_rule(
    "agents/" + _("Agent Plugins"),
    "agent_config:ox_filestore",
    Alternative(
        title = _("Open-Xchange Filestore Check"),
        help = _("This will deploy the agent plugin <tt>ox_filestore</tt> "
                 "for checking Open-Xchange file stores."),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy the OX file stores plugin"),
                elements = [
                    ( "username", TextAscii(title = _("Username for OX admin master"), allow_empty = False )),
                    ( "password", Password(title = _("Password for OX admin master"), allow_empty = False )),
                ],
                optional_keys = False,
            ),
            FixedValue(None, title = _("Do not deploy the OX filestores plugin"), totext = _("(disabled)") ),
        ]
    ),
    match = "first",
)

