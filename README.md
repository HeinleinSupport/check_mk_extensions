# Heinlein check**mk** 2.2 Plugins

This repository contains [check**mk**](https://checkmk.com/) plugins developed by Heinlein Support GmbH and released to the general public.

Development of these plugins can be sponsored by opening a [support request](https://www.heinlein-support.de/consulting) via E-Mail to <support@heinlein-support.de>

## Repository structure

The repository has multiple branches for the specific check**mk** versions.

## To install a plugin

1. download the .mkp file
2. install the plugin ( https://docs.checkmk.com/latest/en/mkps.html?lquery=plugin#commandline )
3. copy the new files from `./local/share/check_mk/agents/plugins` to `/usr/lib/check_mk_agent/plugins`
4. restart the agent
5. perform service discovery.
