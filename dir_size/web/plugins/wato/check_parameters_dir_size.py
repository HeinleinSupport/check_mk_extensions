#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_check_parameters(
    subgroup_storage,
    "dir_size",
    _("Directory Size Limits"),
    Dictionary(
        help = _("Size of all files and subdirectories"),
        elements = [
            ( 'unit',
            DropdownChoice(
                title = _('Unit for Levels'),
                choices = [ ( 'TB', 'Terabytes' ),
                            ( 'GB', 'Gigabytes' ),
                            ( 'MB', 'Megabytes' ),
                            ( 'KB', 'Kilobytes' ),
                            ( 'B', 'Bytes' ),
                          ],
                default_value = 'MB',
            )),
            ('warn', Integer(title = _("Warning at"))),
            ('crit', Integer(title = _("Critical at"))),
        ]
    ),
    TextAscii(
        title = _("Directory"),
        allow_empty = False,
    ),
    match_type = "dict",
)

