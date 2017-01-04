#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_check_parameters(
    subgroup_storage,
    "dir_size_ls",
    _("Directory Size Limits (itself)"),
    Tuple(
        help = _("Size of the directory itself."),
        elements = [
            DropdownChoice(
                title = _('Unit for Levels'),
                choices = [ ( 'TB', 'Terabytes' ),
                            ( 'GB', 'Gigabytes' ),
                            ( 'MB', 'Megabytes' ),
                            ( 'KB', 'Kilobytes' ),
                            ( 'B', 'Bytes' ),
                          ],
                default_value = 'MB',
            ),
            Integer(title = _("Warning at")),
            Integer(title = _("Critical at")),
        ]
    ),
    TextAscii(
        title = _("Directory"),
        allow_empty = False,
    ),
    match_type = "first",
)

