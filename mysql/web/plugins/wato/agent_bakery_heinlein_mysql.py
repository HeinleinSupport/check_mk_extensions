register_rule(group,
    "agent_config:heinlein_mysql",
    Alternative(
        title = _("MySQL Databases (Heinlein)"),
        help = _("This will deploy the agent plugin <tt>heinlein_mysql</tt> on linux systems "
                 "for monitoring several aspects of MySQL databases. It does not include the capacity computation."),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy the MySQL plugin"),
                elements = [
                    ("credentials", Tuple(
                        title = _("Credentials to access the Database"),
                        elements = [
                            TextAscii(
                                title = _("User ID"),
                                default_value = "monitoring",
                            ),
                            Password(
                                title = _("Password")
                            ),
                        ]
                    )),
                    ("socket", TextAscii(
                                title=_("Socket"),
                                default_value = "/var/run/mysqld/mysqld.sock")),
                    ("interval", Age(
                        title = _("Run asynchronously"),
                        label = _("Interval for collecting data"),
                        default_value = 300
                    )),
                ],
            ),
            FixedValue(None, title = _("Do not deploy the MySQL plugin"), totext = _("(disabled)") ),
        ]
    )
)

