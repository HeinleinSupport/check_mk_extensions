#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2013 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from collections.abc import Mapping # type: ignore
from cmk.rulesets.v1 import Help, Label, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
    InputHint,
    Integer,
    LevelDirection,
    ServiceState,
    SimpleLevels,
    SingleChoice,
    SingleChoiceElement,
    String,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import ActiveCheck, Topic

# from pprint import pformat # type: ignore
# import logging
# logger = logging.getLogger(__name__)

_DAY = 24.0 * 3600.0

def _migrate_imap(raw_value: object) -> Mapping[str, object]:
    state_value = {
        'ok': 0,
        'warn': 1,
        'crit': 2,
        'unknown': 3,
    }
    # logger.warning("INVOKE _migrate_imap")
    # logger.warning("raw_value: %s" % pformat(raw_value))

    if not isinstance(raw_value, tuple):
        # logger.warning("raw_value is not a tuple.")
        return raw_value
    
    new_value = {
        "service_desc": raw_value[0],
    }
    settings = raw_value[1]
    new_value["settings"] = settings.copy()
    if "hostname" in settings:
        new_value["hostname"] = settings["hostname"]
        del(new_value["settings"]["hostname"])
    else:
        new_value["hostname"] = "$HOSTADDRESS$"
    if "refuse" in settings:
        new_value["settings"]["refuse"] = state_value.get(settings["refuse"])
    if "mismatch" in settings:
        new_value["settings"]["mismatch"] = state_value.get(settings["mismatch"])
    if "certificate_age" in settings:
        new_value["settings"]["certificate_age"] = ('fixed', (settings["certificate_age"][0] * _DAY, settings["certificate_age"][1] * _DAY))
    warning = None
    critical = None
    if "warning" in settings:
        warning = float(settings["warning"])
        del(new_value["settings"]["warning"])
    if "critical" in settings:
        critical = float(settings["critical"])
        del(new_value["settings"]["critical"])

    if warning or critical:
        if not warning:
            warning = critical
        if not critical:
            critical = 9999.999

        new_value["settings"]["response_time"] = ("fixed", (warning, critical))

    # logger.warning("new_value: %s" % pformat(new_value))
    
    return new_value

def _valuespec_service_desc() -> String:
    return String(
                title = Title("Service Description"),
                prefill = DefaultValue("IMAP"),
            )

def _valuespec_settings() -> Dictionary:
    return Dictionary(
        title = Title("Optional Values"),
        elements = {
            "port": DictElement(
                parameter_form=Integer(
                    title = Title("Port number"),
                    # minvalue = 1,
                    # maxvalue = 65535,
                    prefill = DefaultValue(143),
                )),
            "ip_version": DictElement(
                parameter_form=SingleChoice(
                    title = Title("IP-Version"),
                    elements = [
                        SingleChoiceElement(
                            name="ipv4",
                            title = Title("IPv4"),
                        ),
                        SingleChoiceElement(
                            name="ipv6",
                            title = Title("IPv6"),
                        ),
                    ],
                )),
            "send": DictElement(
                parameter_form=String(
                    title = Title("String to send to the server"),
                )),
            "expect": DictElement(
                parameter_form=String(
                    title = Title("String to expect in server response"),
                )),
            "quit": DictElement(
                parameter_form=String(
                    title = Title("String to send server to initiate a clean close of the connection"),
                )),
            "refuse": DictElement(
                parameter_form=ServiceState(
                    title = Title("Accept TCP refusals with states ok, warn, crit"),
                    prefill = DefaultValue(ServiceState.CRIT),
                )),
            "mismatch": DictElement(
                parameter_form=ServiceState(
                    title = Title("Accept expected string mismatches with states ok, warn, crit"),
                    prefill = DefaultValue(ServiceState.WARN),
                )),
            "jail": DictElement(
                parameter_form=FixedValue(
                    value="jail",
                    title = Title("Hide output from TCP socket"),
                )),
            "maxbytes": DictElement(
                parameter_form=Integer(
                    title = Title("Close connection once more than this number of bytes are received"),
                )),
            "delay": DictElement(
                parameter_form=Integer(
                    title = Title("Seconds to wait between sending string and polling for response"),
                )),
            "ssl": DictElement(
                parameter_form=FixedValue (
                    value="ssl",
                    title = Title("Use SSL for the connection"),
                )),
            "certificate_age": DictElement(
                parameter_form=SimpleLevels[float](
                    title = Title("Minimum number of days a certificate has to be valid."),
                    form_spec_template=TimeSpan(displayed_magnitudes=[TimeMagnitude.DAY]),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=InputHint((90.0 * _DAY, 60 * _DAY)),
                )),
            "response_time": DictElement(
                parameter_form=SimpleLevels[float](
                    title = Title("Maximum response time."),
                    form_spec_template=TimeSpan(displayed_magnitudes=[TimeMagnitude.SECOND, TimeMagnitude.MILLISECOND]),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint((1.0, 5.0)),
                )),
            "timeout": DictElement(
                parameter_form=Integer(
                    title = Title("Seconds before connection times out"),
                    unit_symbol = "sec",
                    prefill = DefaultValue(10),
            )),
        },
      )

def _form_active_checks_imap() -> Dictionary:
    return Dictionary(
        elements={
            "service_desc": DictElement(
                parameter_form=_valuespec_service_desc(),
                required=True,
            ),
            "hostname": DictElement(
                required=False,
                parameter_form=String(
                    title = Title("DNS Hostname or IP address"),
                    prefill = DefaultValue("$HOSTADDRESS$"),
            )),
            "settings": DictElement(
                parameter_form=_valuespec_settings(),
                required=True,
            ),
        },
        migrate=_migrate_imap,
    )

rule_spec_imap = ActiveCheck(
    title=Title("Check IMAP"),
    topic=Topic.NETWORKING,
    name="imap",
    parameter_form=_form_active_checks_imap,
)