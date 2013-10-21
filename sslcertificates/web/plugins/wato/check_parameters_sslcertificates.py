#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "checkparams"

subgroup_applications = _("Applications, Processes &amp; Services")

register_check_parameters(
    subgroup_applications,
    "sslcertificates",
    _("Remaining days until an SSL certificate is invalid"),
    Tuple(
          help = _("Days until expiry of certificate"),
          elements = [
              Integer(title = _("Warning at"), unit = _("days"), default_value = 90),
              Integer(title = _("Critical at"), unit = _("days"), default_value = 60),
          ]
    ),
    TextAscii(
        title = _("Name of service"),
        allow_empty = False,
    ),
    None
)

