#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2015 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

group='datasource_programs'

register_rule(group,
    "special_agents:pingdom",
    Dictionary(
            title = _("Credentials for the pingdom API."),
            elements = [
                ( "username",
                  TextAscii(
                      title = _("Username"),
                      allow_empty = False,
                  )
                ),
                ( "password",
                  Password(
                      title = _("Password"),
                      allow_empty = False,
                  )
                ),
                ( "api_key",
                  Password(
                      title = _("API Key"),
                      allow_empty = False,
                  )
                ),
                ( "email",
                  TextAscii(
                      title = _("Account Email"),
                      allow_empty = True,
                  )
                ),
            ],
            optional_keys = False
    ),
    title = _("Check Pingdom via Rest-API"),
    help  = _('This rule set selects the <a href="http://www.pingdom.com/">Pingdom</a> special agent instead of the normal Check_MK Agent '
              'and allows monitoring the monitored services in your Pingdom account. '
              '<b>Important</b>: To make this special agent Pingdom work you will have to provide the '
              '<a href="https://github.com/drcraig/python-restful-pingdom">Python Module for Pingdom REST API</a>. '
              'Put <a href="https://raw.githubusercontent.com/drcraig/python-restful-pingdom/master/pingdom.py">pingdom.py</a> '
              'into the site directory into <tt>~/local/lib/python</tt>. '
              'The agent itself is located in the site directory under <tt>~/share/check_mk/agents/special</tt>.'),
    match = 'first')

