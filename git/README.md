# git check for check\_mk

## Prerequisites

Get the [check\_git](https://github.com/rfay/check_git) nagios plugin and install to your existing nagios monitoring service.

In case of [OMD - The Open Monitoring Distribution](http://omdistro.org/), you need to copy the actual nagios plugin to ```/opt/omd/versions/$OMD_VERSION/lib/nagios/plugins``` and make it executable.

```
cd /opt/omd/versions/$OMD_VERSION/lib/nagios/plugins
wget https://raw.githubusercontent.com/rfay/check_git/master/check_git
wget https://raw.githubusercontent.com/rfay/check_git/master/check_git_exec_ssh.sh
chmod +x check_git*
```

## Installation

Clone the repo and install the [Check_MK Package](https://mathias-kettner.de/checkmk_packaging.html) with ```check_mk -vP install git-1.0.mkp```. If you are using OMD, you need to become the user of your OMD environment before, (e.g. ```su - prod```).
