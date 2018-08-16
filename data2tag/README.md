# Description #

data2tag is a tool that uses the check_MK Multisite and WATO APIs to set host tags based on information from the monitoring system (e.g. HW/SW-inventory).

data2tag queries a Multisite view (which has to contain at least a column with host names) and sets tags by using a mapping from a configuration file.

# Prequisites #

data2tag needs the [https://github.com/HeinleinSupport/check_mk/tree/master/checkmkapi](checkmkapi) Python module.
