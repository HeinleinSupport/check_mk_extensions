# Cachet Notification Plugin

## Prerequisites

You need an API key from a [Cachet](https://cachethq.io/) instance.

You need php-curl installed on the monitoring server.

## Usage

The notification plugin can be used as any other notification method in check_MK's notification rules.

The Cachet component name is taken from the contact alias. Every Cachet component needs a contact (user) configured with its name as alias. Assign the contacts via contact groups to the services and make sure that only these contacts are using the method "Cachet Dashboard".

## Thanks

The original cachet_notify is from https://github.com/mpellegrin/nagios-eventhandler-cachet
