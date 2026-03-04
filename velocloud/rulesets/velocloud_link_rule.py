#!/usr/bin/env python3

from cmk.gui.i18n import _

from cmk.gui.plugins.wato.utils import (
    rulespec_registry,
    CheckParameterRulespecWithItem,
    RulespecGroupCheckParametersApplications,
)

from cmk.gui.valuespec import (
    Dictionary,
    Float,
    TextAscii,
    Tuple,
)


def _item_spec_velocloud_link():
    return TextAscii(
        title=_("Item"),
    )


def _parameter_valuespec_velocloud_link():
    return Dictionary(
        required_keys=[],
        elements=[
            (
                "rx_latency",
                Tuple(
                    title=_("Upper RX Latency Levels"),
                    elements=[
                        Float(
                            title=_("Warning at"),
                            default_value=20,
                            unit="ms",
                            display_format="%.3f",
                        ),
                        Float(
                            title=_("Critical at"),
                            default_value=50,
                            unit="ms",
                            display_format="%.3f",
                        ),
                    ],
                ),
            ),
            (
                "tx_latency",
                Tuple(
                    title=_("Upper TX Latency Levels"),
                    elements=[
                        Float(
                            title=_("Warning at"),
                            default_value=20,
                            unit="ms",
                            display_format="%.3f",
                        ),
                        Float(
                            title=_("Critical at"),
                            default_value=50,
                            unit="ms",
                            display_format="%.3f",
                        ),
                    ],
                ),
            ),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="velocloud_link",
        group=RulespecGroupCheckParametersApplications,
        parameter_valuespec=_parameter_valuespec_velocloud_link,
        item_spec=_item_spec_velocloud_link,
        title=lambda: _("VeloCloud Link thresholds"),
    )
)
