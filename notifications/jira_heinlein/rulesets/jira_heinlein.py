#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2018 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2. This file is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.rulesets.v1 import (
    Help,
    Title,
)
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    Integer,
    InputHint,
    migrate_to_password,
    Password,
    String,
    validators,
)
from cmk.rulesets.v1.rule_specs import (
    NotificationParameters,
    Topic,
)

def _migrate_password(model):
    print(f"migrating password: {model}")
    if isinstance(model, str):
        model = ("password", model)
        print(f"intermediate password: {model}")
    model = migrate_to_password(model)
    print(f"migrated password: {model}")
    return model

def _valuespec_jira_heinlein() -> Dictionary:
    return Dictionary(
        title=Title("Configure the JIRA connection"),
        elements = {
            "url": DictElement(
                # required=True,
                parameter_form=String(
                    title=Title("JIRA URL"),
                    help_text=Help("Configure the JIRA URL here."),
                    prefill=InputHint(
                        "https://subdomain.domain.tld:port/path/to/jira"
                    ),
                    custom_validate=(
                        validators.Url(
                            [
                                validators.UrlProtocol.HTTP,
                                validators.UrlProtocol.HTTPS,
                            ],
                        ),
                    ),
            )),
            "username": DictElement(
                # required=True,
                parameter_form=String(
                    title = Title("User Name"),
                    help_text = Help("Configure the user name here."),
                    field_size = 40,
            )),
            "password": DictElement(
                # required=True,
                parameter_form=Password(
                    title = Title("Password"),
                    help_text = Help("You need to provide a valid passowrd to be able to send notifications."),
                    migrate=_migrate_password,
            )),
            "monitoring": DictElement(
                parameter_form=String(
                    title=Title("Monitoring URL"),
                    help_text=Help("Configure the base URL for the Monitoring Web-GUI here. Include the site name. This will generate a link in the JIRA issue."),
                    prefill=InputHint(
                        "https://subdomain.domain.tld/sitename/"
                    ),
                    custom_validate=(
                        validators.Url(
                            [
                                validators.UrlProtocol.HTTP,
                                validators.UrlProtocol.HTTPS,
                            ],
                        ),
                    ),
            )),
            "project": DictElement(
                parameter_form=Integer(
                    title = Title("Project ID"),
                    help_text = Help("The numerical JIRA project ID. If not set, it will be retrieved from a custom user attribute named <tt>jiraproject</tt>. If that is not set, the notification will fail."),
            )),
            "issuetype": DictElement(
                parameter_form=Integer(
                    title = Title("Issue type ID"),
                    help_text = Help("The numerical JIRA issue type ID. If not set, it will be retrieved from a custom user attribute named <tt>jiraissuetype</tt>. If that is not set, the notification will fail."),
            )),
            "priority": DictElement(
                parameter_form=Integer(
                    title = Title("Priority ID"),
                    help_text = Help("The numerical JIRA priority ID. If not set, it will be retrieved from a custom user attribute named <tt>jirapriority</tt>. If that is not set, the standard priority will be used."),
            )),
            "resolution": DictElement(
                parameter_form=Integer(
                    title = Title("Resolution Transistion ID"),
                    help_text = Help("The numerical JIRA resolution transition ID. If not set, it will be retrieved from a custom user attribute named <tt>jiraresolution</tt>."),
            )),
            "host_customid": DictElement(
                # required=True,
                parameter_form=Integer(
                    title = Title("Hostproblem-ID custom field ID"),
                    help_text = Help("The numerical custom field ID for the ID number of the host problem."),
            )),
            "service_customid": DictElement(
                # required=True,
                parameter_form=Integer(
                    title = Title("Serviceproblem-ID custom field ID"),
                    help_text = Help("The numerical custom field ID for the ID number of the service problem."),
            )),
            "site_customid": DictElement(
                parameter_form=Integer(
                    title = Title("Site custom field ID"),
                    help_text = Help("The numerical custom field ID for the site name."),
            )),
            "add_customfield": DictElement(
                parameter_form=Integer(
                    title = Title("Additional custom field ID"),
                    help_text = Help("The numerical ID of an additional Jira custom field that should be set in the issue. If not set, it can be retrieved from a custom user attribute named <tt>jiraaddcf</tt>."),
            )),
            "add_customvalue": DictElement(
                parameter_form=String(
                    title = Title("Additional custom field value"),
                    help_text = Help("The value of the additional Jira custom field. If not set, it can be retrieved from a custom user attribute named <tt>jiraaddcfval</tt>."),
            )),
        }
    )

rule_spec_notification_jira_heinlein = NotificationParameters(
    name="jira_heinlein",
    title=Title("JIRA (Heinlein)"),
    parameter_form=_valuespec_jira_heinlein,
    topic=Topic.NOTIFICATIONS,
)
