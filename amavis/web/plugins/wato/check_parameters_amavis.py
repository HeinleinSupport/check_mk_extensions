#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_check_parameters(
    subgroup_applications,
    "amavis",
    _("Amavis Statistics"),
    Dictionary(
        elements = [
            ( 'busy_childs',
            Tuple(
                title = _("Busy child processes"),
                elements = [
                    Integer(title = _("Warning at"), unit='%', default_value=75),
                    Integer(title = _("Critical at"), unit='%', default_value=95),
                ]
            )),
        ],
        optional_keys = [],
    ),
    None,
    match_type = "dict",
)

