checkgroups = []
subgroup_os =           _("Operating System Resources")

register_check_parameters(
     subgroup_os,
    "entropy_avail",
    _("Entropy Available"),
    Dictionary(
        help = _("Here you can override the default levels for the entropy Available check."
                   "You can either specify a absolut value or a percentage value."),
        elements = [
            ( "percentage",
                Tuple(
                title = _("Minimum Entropy that has to be available in percent"),
                elements = [
                    Percentage(title = _("Warning at"), default_value = 0.0, unit = _("% left")),
                    Percentage(title = _("Critical at"), default_value = 0.0, unit = _("% left")),
                ]
                )
            ),
            ( "absolute",
                Tuple(
                title = _("Minimum absolute Entropy that has to be available"),
                elements = [
                    Integer(title = _("Warning if below than"), default_value = 200),
                    Integer(title = _("Critical if below than"), default_value = 100),
                ],
                ),
            ),
        ],
    ),
    None,
    match = "dict",
)
