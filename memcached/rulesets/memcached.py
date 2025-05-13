#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.rulesets.v1 import (
    Title,
)
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    InputHint,
    Float,
    LevelDirection,
    migrate_to_integer_simple_levels,
    migrate_to_float_simple_levels,
    SimpleLevels,
    String,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    HostCondition,
    Topic,
)

def migrate_version_tuple_to_dict(model):
    match model:
        case None | (None, None):
            return None
        case (str(warn), str(crit)):
            return { "warn": warn, "crit": crit }
        case { "warn": str(warn), "crit": str(crit) }:
            return model
        case _:
            raise TypeError(f"Could not migrate {model!r} to SimpleLevelsConfigModel.")

def memcached_dict_element(title, warn, crit, direction, unit):
    spec_type = {
        int: Integer,
        float: Float,
    }
    migrate_func = {
        int: migrate_to_integer_simple_levels,
        float: migrate_to_float_simple_levels,
    }
    warn_type = type(warn)
    sl = SimpleLevels(
        title=Title(title),
        migrate=migrate_func[warn_type],
        form_spec_template=spec_type[warn_type](
            unit_symbol=unit,
        ),
        level_direction=direction,
        prefill_fixed_levels=DefaultValue((warn, crit)),
    )
    return DictElement(
        parameter_form=sl,
    )

def memcached_upper_bounds(title, warn, crit, unit=None):
    return memcached_dict_element(title, warn, crit, LevelDirection.UPPER, unit)

def memcached_lower_bounds(title, warn, crit, unit=None):
    return memcached_dict_element(title, warn, crit, LevelDirection.LOWER, unit)

def _parameter_valuespec_memcached():
    return Dictionary(
        title = Title("Limits"),
        elements = {
            'version':               DictElement(
                parameter_form=Dictionary(
                    title=Title("Version"),
                    migrate=migrate_version_tuple_to_dict,
                    elements={
                        "warn": DictElement(
                            required=True,
                            parameter_form=String(
                                title=Title("Warning below"),
                                prefill=InputHint("1.5.6"),
                            )
                        ),
                        "crit": DictElement(
                            required=True,
                            parameter_form=String(
                                title=Title("Critical below"),
                                prefill=InputHint("1.4.15"),
                            )
                        ),
                    },
                ),
            ),
            'pointer_size':          memcached_lower_bounds("Architecture",
                                                            64,      32,
                                                            "bits"),
            'rusage_system':         memcached_upper_bounds("System CPU time used",
                                                             0,        0,
                                                             "s"),
            'rusage_user':           memcached_upper_bounds("User CPU time used",
                                                             0,        0,
                                                             "s"),
            'threads':               memcached_upper_bounds("Number of threads used",
                                                             0,        0),
            'auth_cmds':             memcached_upper_bounds("Number of authentication commands",
                                                             0,        0,
                                                             "per second"),
            'auth_errors':           memcached_upper_bounds("Number of authentication errors",
                                                             0,        0,
                                                             "per second"),
            'bytes_percent':         memcached_upper_bounds("Cache Usage",
                                                             80.0,     90.0,
                                                             "percent"),
            'bytes_read':            memcached_upper_bounds("Bytes Read",
                                                             0,        0,
                                                             "per second"),
            'bytes_written':         memcached_upper_bounds("Bytes Written",
                                                             0,        0,
                                                             "per second"),
            'curr_items':            memcached_upper_bounds("Number of items in cache",
                                                             0,        0),
            'evictions':             memcached_upper_bounds("Number of objects removed to free up memory",
                                                             100,      200,
                                                             "per second"),
            'get_hits':              memcached_upper_bounds("Number of successful 'get' commands",
                                                             0,        0,
                                                             "per second"),
            'get_misses':            memcached_upper_bounds("Number of failed 'get' commands",
                                                             0,        0,
                                                             "per second"),
            'total_connections':     memcached_upper_bounds("Number of connections",
                                                             0,        0,
                                                             "per second"),
            'total_items':           memcached_upper_bounds("Number of items stored on the server",
                                                             0,        0,
                                                             "per second"),
            'cache_hit_rate':        memcached_lower_bounds("Rate of cache hits",
                                                             20,       10,
                                                             "percent"),
            'cas_badval':            memcached_upper_bounds("CAS fails due to bad identifier",
                                                             5,        10,
                                                             "per second"),
            'cas_hits':              memcached_upper_bounds("CAS hits",
                                                             0,        0,
                                                             "per second"),
            'cas_misses':            memcached_upper_bounds("CAS misses",
                                                             0,        0,
                                                             "per second"),
            'cmd_flush':             memcached_upper_bounds("Number of 'flush_all' commands",
                                                             1,        5,
                                                             "per second"),
            'cmd_get':               memcached_upper_bounds("Number of 'get' commands",
                                                             0,        0,
                                                             "per second"),
            'cmd_set':               memcached_upper_bounds("Number of 'set' commands",
                                                             0,        0,
                                                             "per second"),
            'connection_structures': memcached_upper_bounds("Internal connection handles",
                                                             0,        0),
            'curr_connections':      memcached_upper_bounds("Open Connections",
                                                             0,        0),
            'listen_disabled_num':   memcached_upper_bounds("Connection fails due to connection limit",
                                                             5,        10,
                                                             "per second"),
            'conn_yields':           memcached_upper_bounds("Forced connection yields",
                                                             1,        5,
                                                             "per second"),
            'decr_hits':             memcached_upper_bounds("Number of succesful decr commands",
                                                             0,        0,
                                                             "per second"),
            'decr_misses':           memcached_upper_bounds("Number of failed decr commands",
                                                             0,        0,
                                                             "per second"),
            'incr_hits':             memcached_upper_bounds("Number of successful incr commands",
                                                             0,        0,
                                                             "per second"),
            'incr_misses':           memcached_upper_bounds("Number of failed incr commands",
                                                             0,        0,
                                                             "per second"),
            'delete_hits':           memcached_upper_bounds("Cache hits on delete",
                                                             0,        0,
                                                             "per second"),
            'delete_misses':         memcached_upper_bounds("Cache misses on delete",
                                                             1000,     2000,
                                                             "per second"),
            'reclaimed':             memcached_upper_bounds("Number of times a request used memory from an expired key",
                                                             0,        0,
                                                             "per second"),
        },
    )

rule_spec_memcached = CheckParameters(
    name="memcached",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_memcached,
    title=Title("Parameters for Memcached"),
    condition=HostAndItemCondition(
        item_title=Title("Instance"),
        item_form=String(),
    ),
)
