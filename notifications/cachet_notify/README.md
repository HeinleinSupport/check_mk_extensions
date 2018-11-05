# Cachet Notification Plugin

## Prerequisites

You need an API key from a [Cachet](https://cachethq.io/) instance.

## Usage

The notification plugin can be used as any other notification method in check_MK's notification rules.

It does not need a specific contact as destination but you need to configure an explicit email address as dummy destination.

You need to set the Cachet component name in the notification rule. I.e. you need separate notification rules for every Cachet component.
