#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2013 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

group = "activechecks"

register_rule(group,
              "active_checks:mongodb",
              Tuple(
                  title = _("Check MongoDB"),
                  help = _("Checks MongoDB via TCP."),
                  elements = [
                      DropdownChoice(
                          title = _("Action"),
                          choices = [
                              ('connect', 'Connect'),
                              ('asserts', 'Asserts'),
                              ('chunks_balance', 'Chunks Balance'),
                              ('collection_indexes', 'Collection Indexes'),
                              ('collections', 'Collections'),
                              ('collection_state', 'Collection State'),
                              ('connections', 'Connections'),
                              ('connect_primary', 'Connect Primary'),
                              ('current_lock', 'Current Lock'),
                              ('database_indexes', 'Database Indexes'),
                              ('databases', 'Databases'),
                              ('database_size', 'Database Size'),
                              ('flushing', 'Flushing'),
                              ('index_miss_ratio', 'Index Miss Ratio'),
                              ('journal_commits_in_wl', 'Journal Commits in WL'),
                              ('journaled', 'Journaled'),
                              ('last_flush_time', 'last flush time'),
                              ('lock', 'lock'),
                              ('memory', 'memory'),
                              ('memory_mapped', 'memory mapped'),
                              ('opcounters', 'opcounters'),
                              ('oplog', 'oplog'),
                              ('page_faults', 'page faults'),
                              ('queries_per_second', 'queries per second'),
                              ('queues', 'queues'),
                              ('replica_primary', 'replica primary'),
                              ('replication_lag', 'replication lag'),
                              ('replication_lag_percent', 'replication lag percent'),
                              ('replset_state', 'replset state'),
                              ('row_count', 'row count'),
                              ('write_data_files', 'write data files'),
                              ],
                          ),
                      Dictionary(
                          title = _("Global parameters"),
                          elements = [
                              ( "hostname",
                                TextAscii(
                                    title = _("DNS Hostname or IP address"),
                                    default_value = "$HOSTADDRESS$",
                                    allow_empty = False,
                                    help = _("You can specify a hostname or IP address different from IP address "
                                             "of the host as configured in your host properties."))),
                              ( 'port',
                                Integer(
                                    title = _("MongoDB Port"),
                                    help = _("Default is 27017."),
                                    minvalue = 1,
                                    maxvalue = 65535,
                                    default_value = 27017)),
                              ( "user",
                                TextAscii(
                                    title = _("Username"),
                                    help = _("The username you want to login as"),
                                    size = 30)
                                ),
                              ( "pass",
                                Password(
                                    title = _("Password"),
                                    help = _("The password you want to use for that user"),
                                    size = 30)
                                ),
                              ( "warning",
                                Integer(
                                    title = _("Warning"),
                                    help = _("The warning threshold we want to set"),
                                    size = 10,
                                    )
                                ),
                              ( "critical",
                                Integer(
                                    title = _("Critical"),
                                    help = _("The critical threshold we want to set"),
                                    size = 10,
                                    )
                                ),
                              ( 'database',
                                Alternative(
                                    title = _("Databases"),
                                    elements = [
                                        TextAscii(
                                            title = _("Database Name"),
                                            help = _("Specify the database to check"),
                                            ),
                                        Checkbox(
                                            title = _("All Databases"),
                                            label = _("Check all databases (action database_size)"),
                                            true_label = "All Databases",
                                            ),
                                        ]
                                    )
                                ),
                              ( "querytype",
                                DropdownChoice(
                                    title = _("Query Type"),
                                    help = _("The query type to check (from queries_per_second)"),
                                    choices = [
                                        ( 'query', 'Query' ),
                                        ( 'insert', 'Insert' ),
                                        ( 'update', 'Update' ),
                                        ( 'delete', 'Delete' ),
                                        ( 'getmore', 'Get More' ),
                                        ( 'command', 'Command' ),
                                        ],
                                    )
                                ),
                              ( "collectionset",
                                TextAscii(
                                    title = _("Collection"),
                                    help = _("Specify the collection to check"),
                                    )
                                ),
                              ( "sampletime",
                                Integer(
                                    title = _("Sample Time"),
                                    help = _("Time used to sample number of pages faults"),
                                    )
                                ),
                              ]
                          ),
                      Checkbox(
                          title = _("Replication Lag"),
                          label = _("Get max replication lag (for replication_lag action only)"),
                          true_label = _("Get max replication lag"),
                          false_label = _("Ignore replication lag"),
                          ),
                      Checkbox(
                          title = _("Mapped Memory"),
                          label = _("Get mapped memory instead of resident (if resident memory can not be read)"),
                          true_label = _("Get mapped memory"),
                          false_label = _("Get resident memory"),
                          ),
                      Checkbox(
                          title = _("SSL"),
                          label = _("Connect using SSL"),
                          true_label = _("using SSL"),
                          false_label = _("without SSL"),
                          ),
                      Checkbox(
                          title = _("Replica Set"),
                          label = _("Connect to replicaset"),
                          true_label = _("Connect to replicaset"),
                          false_label = _("No replicaset"),
                          ),
                      Checkbox(
                          title = _("Performance Data"),
                          label = _("Enable output of performance data"),
                          true_label = _("with performance data"),
                          false_label = _("withput performance data"),
                          ),
                      ]
                  ),
              match = 'all')
