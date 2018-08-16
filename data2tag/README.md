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

