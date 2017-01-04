#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_check_parameters(
    subgroup_applications,
    "sslcertificates",
    _("Parameters for SSL certificates"),
    Dictionary(
        elements = [
            ('age', Tuple(
                title = _('Certificate Age'),
                help = _("Days until expiry of certificate"),
                elements = [
                    Integer(title = _("Warning at"), unit = _("days"), default_value = 90),
                    Integer(title = _("Critical at"), unit = _("days"), default_value = 60),
                ])),
            ('warnalgo',
             ListOfStrings(
                 title = _('Signature Algorithms that generate WARNs'),
                 default_value = ['md5WithRSAEncryption', 'sha1WithRSAEncryption']
                 ))
        ],
    ),
    TextAscii(
        title = _("Name of service"),
        allow_empty = False,
    ),
    'dict',
)

