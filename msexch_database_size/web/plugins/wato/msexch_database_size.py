#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithItem,
    RulespecGroupCheckParametersApplications,
)
from cmk.gui.valuespec import (
    DropdownChoice,
    Filesize,
    Optional,
    TextAscii,
    Tuple,
)

def _item_spec_msexch_database_size():
    return TextAscii(
        title=_("Name of the database"),
    )

def _transform_msexch_database_size(source):
  if isinstance(source, dict):
      return source
  return {"size": source}
def _parameter_valuespec_msexch_database_size():
    return Transform(Dictionary(
            optional_keys=['size','availSpace'],
            title=_("Thresholds for total database size or percentage of free space within the database."),
            help=_("Deleting old mailboxes leads to white space that MS Exchange administrators might want to clean up."),
            elements = [('size',
                Tuple(
                    help=_("The check will trigger a warning or critical state if the size of the "
                       "database exceeds these levels."),
                    title=_("Impose limits on the size of the database"),
                    elements=[
                        Filesize(title=_("warning at")),
                        Filesize(title=_("critical at")),
                    ]),
               ),
               ('availSpace',
                    Tuple(title=_('Percentage of free Mailbox space'),
                                   elements=[
                                       Percentage(title=_("Warning at")),
                                       Percentage(title=_("Critical at")),
                                   ],
                    default_value=(20.0, 40.0),),
               ),
            ]
        ),
        forth=_transform_msexch_database_size,
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="msexch_database_size",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_msexch_database_size,
        parameter_valuespec=_parameter_valuespec_msexch_database_size,
        title=lambda: _("MS Exchange Database Size"),
    ))
