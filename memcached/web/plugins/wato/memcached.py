def memcached_upper_bounds(title, warn, crit, unit = None):
    spec_type = {
        int: Integer,
        float: Float,
        str: TextAscii
    }
    return Tuple(
        title = title,
        elements = [
            spec_type[type(warn)](title = _("Warning at"), unit = unit, default_value = warn),
            spec_type[type(warn)](title = _("Critical at"), unit = unit, default_value = crit),
        ]
    )

def memcached_lower_bounds(title, warn, crit, unit=None):
    spec_type = {
        int: Integer,
        float: Float,
        str: TextAscii
    }
    return Tuple(
        title = title,
        elements = [
            spec_type[type(warn)](title = _("Warning below"), unit = unit, default_value = warn),
            spec_type[type(warn)](title = _("Critical below"), unit = unit, default_value = crit),
        ]
    )

register_check_parameters(
    subgroup_applications,
    "memcached",
    _("Memcached"),
    Dictionary(
        title = _("Limits"),
        elements = [
            ('version',               memcached_lower_bounds("Version",
                                                             "1.4.15", "1.4.15")),
            ('pointer_size',          memcached_lower_bounds("Architecture",
                                                             64,       32)),
            ('rusage_system',         memcached_upper_bounds("System CPU time used",
                                                             0,        0, u"s")),
            ('rusage_user',           memcached_upper_bounds("User CPU time used",
                                                             0,        0, u"s")),
            ('threads',               memcached_upper_bounds("Number of threads used",
                                                             0,        0)),
            ('auth_cmds',             memcached_upper_bounds("Number of authentication commands",
                                                             0,        0, _("per second"))),
            ('auth_errors',           memcached_upper_bounds("Number of authentication errors",
                                                             0,        0, _("per second"))),
            ('bytes_percent',         memcached_upper_bounds("Cache Usage",
                                                             80,       90, _("percent"))),
            ('bytes_read',            memcached_upper_bounds("Bytes Read",
                                                             0,        0, _("per second"))),
            ('bytes_written',         memcached_upper_bounds("Bytes Written",
                                                             0,        0, _("per second"))),
            ('curr_items',            memcached_upper_bounds("Number of items in cache",
                                                             0,        0)),
            ('evictions',             memcached_upper_bounds("Number of objects removed to free up memory",
                                                             100,      200, _("per second"))),
            ('get_hits',              memcached_upper_bounds("Number of successful 'get' commands",
                                                             0,        0, _("per second"))),
            ('get_misses',            memcached_upper_bounds("Number of failed 'get' commands",
                                                             0,        0, _("per second"))),
            ('total_connections',     memcached_upper_bounds("Number of connections",
                                                             0,        0, _("per second"))),
            ('total_items',           memcached_upper_bounds("Number of items stored on the server",
                                                             0,        0, _("per second"))),
            ('cache_hit_rate',        memcached_lower_bounds("Rate of cache hits",
                                                             20,       10, _("percent"))),
            ('cas_badval',            memcached_upper_bounds("CAS fails due to bad identifier",
                                                             5,        10, _("per second"))),
            ('cas_hits',              memcached_upper_bounds("CAS hits",
                                                             0,        0, _("per second"))),
            ('cas_misses',            memcached_upper_bounds("CAS misses",
                                                             0,        0, _("per second"))),
            ('cmd_flush',             memcached_upper_bounds("Number of 'flush_all' commands",
                                                             1,        5, _("per second"))),
            ('cmd_get',               memcached_upper_bounds("Number of 'get' commands",
                                                             0,        0, _("per second"))),
            ('cmd_set',               memcached_upper_bounds("Number of 'set' commands",
                                                             0,        0, _("per second"))),
            ('connection_structures', memcached_upper_bounds("Internal connection handles",
                                                             0,        0)),
            ('curr_connections',      memcached_upper_bounds("Open Connections",
                                                             0,        0)),
            ('listen_disabled_num',   memcached_upper_bounds("Connection fails due to connection limit",
                                                             5,        10, _("per second"))),
            ('conn_yields',           memcached_upper_bounds("Forced connection yields",
                                                             1,        5, _("per second"))),
            ('decr_hits',             memcached_upper_bounds("Number of succesful decr commands",
                                                             0,        0, _("per second"))),
            ('decr_misses',           memcached_upper_bounds("Number of failed decr commands",
                                                             0,        0, _("per second"))),
            ('incr_hits',             memcached_upper_bounds("Number of successful incr commands",
                                                             0,        0, _("per second"))),
            ('incr_misses',           memcached_upper_bounds("Number of failed incr commands",
                                                             0,        0, _("per second"))),
            ('delete_hits',           memcached_upper_bounds("Cache hits on delete",
                                                             0,        0, _("per second"))),
            ('delete_misses',         memcached_upper_bounds("Cache misses on delete",
                                                             1000,     2000, _("per second"))),
            ('reclaimed',             memcached_upper_bounds("Number of times a request used memory from an expired key",
                                                             0,        0, _("per second")))
        ]
    ),
    TextAscii(title = _("Instance")),
    match_type='dict',
)

register_rule("agents/" + _("Agent Plugins"),
    "agent_config:memcached",
    CascadingDropdown(
        title = _("Memcached instances (Linux)"),
        help = _("If you activate this option, then the agent plugin <tt>memcached</tt> will be deployed. "
                 "For each configured or detected memcached instance there will be one new service with detailed "
                 "statistics of the current number of clients and processes and their various states."),
        style = "dropdown",
        choices = [
            ( "autodetect", _("Autodetect instances")
             ),
            ( "static", _("Specific list of instances"),
                ListOf(
                    Tuple(
                        elements = [
                            IPv4Address(
                                title = _("IP Address"),
                                default_value = "127.0.0.1",
                            ),
                            Alternative(
                                style = "dropdown",
                                elements = [
                                    FixedValue(None,
                                        title = _("Don't use custom port"),
                                        totext = _("Use default port"),
                                    ),
                                    Integer(
                                        title = _("TCP Port Number"),
                                        minvalue = 1,
                                        maxvalue = 65535,
                                        default_value = 11211,
                                    ),
                                ]
                            ),
                        ]
                    ),
                ),
            ),
            ( '_no_deploy', _("Do not deploy the memcached plugin") ),
        ]
    ),
)
