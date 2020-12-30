#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Tuple,
    Integer,
    ListOfStrings,
    MonitoringState,
    TextAscii,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithItem,
    RulespecGroupCheckParametersApplications,
)

def _item_spec_sslcertificates():
    return TextAscii(
        title = _("Certificate File"),
        allow_empty = False,
    )

def _parameter_valuespec_sslcertificates():
    return Dictionary(
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
                    TextAscii(title = _('Reason'), allow_empty = False, size = 72),
                ])),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="sslcertificates",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_sslcertificates,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_sslcertificates,
        title=lambda: _("Parameters for SSL certificates"),
    ))
