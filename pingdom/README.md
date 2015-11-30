Pingdom API Check for Nagios and Check_MK
=========================================

This is a Nagios Check-Plugin and a Check_MK special agent using the Pingdom API to check the status of external Pingdom checks.

You need the pingdom Python module available from https://github.com/drcraig/python-restful-pingdom, place it in a folder within your Python path.

Invocation
----------

You can use check_pingdom.py like any other Nagios check plugin.

Use --help for a help text.

There are two operations: "list" and "check".

"list" shows all Pingdom checks available in the account.

"check" checks one Pingdom check identified by its ID.

Check_MK
--------

When using Check_MK install the files into your site and use it as special agent.

There is a new ruleset to assign the special agent Pingdom to a host. Create a host just for this purpose.

The special agent will discover all available checks and create piggyback data for your "real" hosts.
