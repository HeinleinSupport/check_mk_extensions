# Description #

data2tag is a tool that uses the check_MK Multisite and WATO APIs to set host tags based on information from the monitoring system (e.g. HW/SW-inventory).

data2tag queries a Multisite view (which has to contain at least a column with host names) and sets tags by using a mapping from a configuration file.

# Prequisites #

data2tag needs the [checkmkapi](https://github.com/HeinleinSupport/check_mk/tree/master/checkmkapi) Python module.

# Usage #

    data2tag.py --help
	usage: data2tag.py [-h] -s URL -u USERNAME -p PASSWORD -c CONFIG [-d]
    
    optional arguments:
	  -h, --help            show this help message and exit
	  -s URL, --url URL     URL to Check_MK site
      -u USERNAME, --username USERNAME
                            name of the automation user
      -p PASSWORD, --password PASSWORD
                            secret of the automation user
      -c CONFIG, --config CONFIG
                            Path to config file
      -d, --dump            Dump unique values from the view

The config file contains a Python data structure (a dictionary) with at least two keys: view_name and tagmap. The tagmap is a dictionary where the keys are the columns from the view and the values are again dictionaries where the keys are regular expressions that should match the content from the view's column and the value is a dictionary setting the tags. Example:

    {
      'view_name': 'inv_hosts_cpu',
      'tagmap': {
        'inv_software_os_name': {
          'centos'                       : {'tag_opsys': 'redhat'},
          'debian'                       : {'tag_opsys': 'debian'},
          'suse'                         : {'tag_opsys': 'suse'},
          'ubuntu'                       : {'tag_opsys': 'ubuntu'},
          'xenserver'                    : {'tag_opsys': 'redhat'},
          'Microsoft Windows 7'          : {'tag_opsys': 'win7'},
          'Microsoft Windows Server 2008': {'tag_opsys': 'win2008'},
          'Microsoft Windows Server 2012': {'tag_opsys': 'win2012'},
          'Microsoft Windows Server 2016': {'tag_opsys': 'win2016'},
        },
      }
    }

The tag group (e.g. 'opsys') and the tag choices have to exist before running data2tag.

An additional key 'args' may exist in the configuration dictionary which defines view parameters. E.g.:

    {
      'view_name': 'invswpac_search',
      'args': {
        'filled_in': 'filter',
        'invswpac_name': 'apache2$',
      },
      'tagmap': {
        'invswpac_name': {
          'apache2': {'tag_apache': 'apache'},
        },
      }
    }
