#!/usr/bin/env python
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
                 )),
            ('ignore',
             Tuple(
                title = _('Ignore old Certificates'),
                help = _('Set number of days after which an expired certificate is ignored. A reason has to be given.'),
                elements = [
                    Integer(title = _('Ignore after'), unit = _('days'), default_value = 365),
                    TextAscii(title = _('Reason'), allow_empty = False, size = 72, min_len = 5),
                ])),
        ],
    ),
    TextAscii(
        title = _("Certificate File"),
        allow_empty = False,
    ),
    'dict',
)

