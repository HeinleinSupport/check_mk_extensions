#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_rule("agents/" + _("Agent Plugins"),
    "agent_config:filehandles",
    DropdownChoice(
        title = _("Filehandles (Linux)"),
        help = _("This will deploy the agent plugin <tt>filehandles</tt> for monitoring the number of allocated file handles."),
        choices = [
            ( True, _("Deploy filehandles plugin") ),
            ( None, _("Do not deploy filehandles plugin") ),
        ]
    )
)

register_check_parameters(
    subgroup_applications,
    'filehandles',
    _('Filehandles'),
    Dictionary(
        elements = [
            ('levels', Tuple(
                title = _("Filehandles levels"),
                help = _('The global levels are in percentage, the per process levels are absolute values.'),
                elements = [
                    Integer(
                        title = _("Warning at"),
                        default_value = 80,
                    ),
                    Integer(
                        title = _("Critical at"),
                        default_value = 90,
                    ),
                ]
            )),
        ],
        help = _("This rule is used to configure thresholds for filehandles, globally or per process."),
    ),
    TextAscii(
        title = _("Process Name"),
        help = _("Teh process name as defined in the inventory rule or 'global' for the global values."),
    ),
    match_type = "dict",
)

register_rule(
    'checkparams/' + subgroup_inventory,
    varname   = "inventory_filehandles_rules",
    title     = _('Filehandles Discovery'),
    help      = _("This ruleset defines criteria for automatically creating checks for filehandles of running processes "
                  "based upon what is running when the service discovery is done. These services will be "
                  "created with default parameters. They will get critical when no process is running and "
                  "OK otherwise. You can parameterize the check with the ruleset <i>Filehandles</i>."),
    valuespec = Dictionary(
        elements = [
            ('descr', TextAscii(
                title = _('Process Name'),
                style = "dropdown",
                allow_empty = False,
                help  = _('<p>The process name may contain one or more occurances of <tt>%s</tt>. If you do this, then the pattern must be a regular '
                          'expression and be prefixed with ~. For each <tt>%s</tt> in the description, the expression has to contain one "group". A group '
                          'is a subexpression enclosed in brackets, for example <tt>(.*)</tt> or <tt>([a-zA-Z]+)</tt> or <tt>(...)</tt>. When the inventory finds a process '
                          'matching the pattern, it will substitute all such groups with the actual values when creating the check. That way one '
                          'rule can create several checks on a host.</p>'
                          '<p>If the pattern contains more groups then occurrances of <tt>%s</tt> in the service description then only the first matching '
                          'subexpressions  are used for the  service descriptions. The matched substrings corresponding to the remaining groups '
                          'are copied into the regular expression, nevertheless.</p>'
                          '<p>As an alternative to <tt>%s</tt> you may also use <tt>%1</tt>, <tt>%2</tt>, etc. '
                          'These will be replaced by the first, second, ... matching group. This allows you to reorder things.</p>'
                ),
            )),
            ('match', Alternative(
                title = _("Process Matching"),
                style = "dropdown",
                elements = [
                    TextAscii(
                        title = _("Exact name of the process without argments"),
                        label = _("Executable:"),
                        size = 50,
                    ),
                    Transform(
                        RegExp(
                            size = 50,
                            mode = RegExp.prefix,
                        ),
                        title = _("Regular expression matching command line"),
                        label = _("Command line:"),
                        help = _("This regex must match the <i>beginning</i> of the complete "
                                 "command line of the process including arguments"),
                        forth = lambda x: x[1:],   # remove ~
                        back  = lambda x: "~" + x, # prefix ~
                    ),
                    FixedValue(
                        None,
                        totext = "",
                        title = _("Match all processes"),
                    )
                ],
                match = lambda x: (not x and 2) or (x[0] == '~' and 1 or 0),
                default_value = '/usr/sbin/foo',
            )),
            ('user', Alternative(
                title = _('Name of the User'),
                style = "dropdown",
                elements = [
                    FixedValue(
                        None,
                        totext = "",
                        title = _("Match all users"),
                    ),
                    TextAscii(
                        title = _('Exact name of the user'),
                        label = _("User:"),
                    ),
                    FixedValue(
                        False,
                        title = _('Grab user from found processess'),
                        totext = '',
                    ),
                ],
                help = _('<p>The user specification can either be a user name (string). The inventory will then trigger only if that user matches '
                         'the user the process is running as and the resulting check will require that user. Alternatively you can specify '
                         '"grab user". If user is not selected the created check will not check for a specific user.</p>'
                         '<p>Specifying "grab user" makes the created check expect the process to run as the same user as during inventory: the user '
                         'name will be hardcoded into the check. In that case if you put <tt>%u</tt> into the service description, that will be replaced '
                         'by the actual user name during inventory. You need that if your rule might match for more than one user - your would '
                         'create duplicate services with the same description otherwise.</p><p>Windows users are specified by the namespace followed by '
                         'the actual user name. For example "\\\\NT AUTHORITY\NETWORK SERVICE" or "\\\\CHKMKTEST\Administrator".</p>'),
            )),
        ],
        required_keys = [ "descr" ],
    ),
    match = 'all',
)
