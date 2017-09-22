#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Rules for configuring parameters of checks (services)

# subgroup_applications = _("Applications, Processes & Services")

sap_hana_license_elements = [
    ( "license_usage",
        Alternative(
            title = _("Licensed product usage"),
            help  = _("The amount of memory used for the HANA DB."),
            elements = [
                    Tuple(title = _("Percentage used"),
                          elements = [
                               Percentage(title = _("Warning if above"), default_value=80.0),
                               Percentage(title = _("Critical if above"), default_value=90.0),
                          ]
                    ),
                    Tuple(title = _("Absolute used"),
                          elements = [
                               Integer(title = _("Warning if above"),  size = 10, unit = _("GB"), minvalue = 0),
                               Integer(title = _("Critical if above"), size = 10, unit = _("GB"), minvalue = 0),
                          ]
                    )
            ],
            default_value = (80.0, 90.0),
        )
    ),
]

register_check_parameters(
    subgroup_applications,
    "sap_hana_license",
    _("SAP HANA Licensed Memory Usage"),
    Dictionary(
        elements = sap_hana_license_elements,
        hidden_keys = [],
    ),
    TextAscii(
        title = _("Instance"),
        help = _("Specify the SAP HANA instance name"),
        allow_empty = False),
    "dict"
)
