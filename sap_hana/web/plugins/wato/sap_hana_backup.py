subgroup_applications = _("Applications, Processes & Services")

register_check_parameters(
        subgroup_applications,
        "sap_hana_backup",
        _("SAP HANA Backup Age"),
        Dictionary(
                help = _("This check monitors the age of a SAP HANA Backup"),
                elements = [
                        ("backup_age",
                                Tuple(
                                         title = _("Maximum time since a backup job last ran"),
                                         elements = [
                                                     Float(title = _("Warning if more than") , unit = "hours", minvalue = 0.0, default_value="24"),
                                                     Float(title = _("Critical if more than"), unit = "hours", minvalue = 0.0, default_value="48"),
                                                    ]
                                     ),
                                ),
                        ],
            ),
        TextAscii(
                title = _("Job Type"),
                allow_empty = True
        ),
        "dict",
)
