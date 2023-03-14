### checkmkapi.`_check_mk_url` [function]
adds trailing check_mk path component to URL 
### checkmkapi.`_site_url` [function]
None
### checkmkapi.`_site_creds` [function]
None
### checkmkapi.`CMKRESTAPI` [class]
None
#### CMKRESTAPI.`__init__`
Initialize a REST-API instance. URL, User and Secret can be automatically taken from local site if running as site user.

Args:
    site_url: the site URL
    api_user: username of automation user account
    api_secret: automation secret

Returns:
    instance of CMKRESTAPI
#### CMKRESTAPI.`_check_response`
None
#### CMKRESTAPI.`_get_url`
None
#### CMKRESTAPI.`_post_url`
None
#### CMKRESTAPI.`_put_url`
None
#### CMKRESTAPI.`_delete_url`
None
#### CMKRESTAPI.`add_host`
Adds a host to a folder in the CheckMK configuration.

Args:
    hostname: unique name for the new host
    folder: The folder-id of the folder under which this folder shall be created. May be 'root' for the root-folder.

Returns:
    (data, etag)
    data: host's data
    etag: current etag value
#### CMKRESTAPI.`get_host`
Gets host configuration including eTag value.

Args:
    hostname:  A hostname
    effective_attr: Show all effective attributes, which affect this host, not just the attributes which were set on this host specifically. This includes all attributes of all of this host's parent folders.

Returns:
    (data, etag)
    data: host's data
    etag: current etag value
#### CMKRESTAPI.`get_all_hosts`
Gets all hosts from the CheckMK configuration.

Args:
    effective_attr: Show all effective attributes, which affect this host, not just the attributes which were set on this host specifically. This includes all attributes of all of this host's parent folders.
    attributes: If False do not fetch hosts' data

Returns:
    hosts: Dictionary of host data or dict of hostname -> URL depending on aatributes parameter
#### CMKRESTAPI.`delete_host`
Deletes a host from the CheckMK configuration.

Args:
    hostname: name of the host

Returns:
    (data, etag)
    data: host's data
    etag: current etag value
#### CMKRESTAPI.`edit_host`
Edit a host in the CheckMK configuration.

Args:
    hostname: name of the host
    etag: (optional) etag value, if not provided the host will be looked up first using get_host().
    set_attr: Replace all currently set attributes on the host, with these attributes. Any previously set attributes which are not given here will be removed.
    update_attr: Just update the hosts attributes with these attributes. The previously set attributes will not be touched.
    unset_attr: A list of attributes which should be removed.

Returns:
    (data, etag)
    data: host's data
    etag: current etag value
#### CMKRESTAPI.`disc_host`
Discovers services on a host.

Args:
    hostname: name of the host

Returns:
    (data, etag)
    data: discovery data
    etag: current etag value
#### CMKRESTAPI.`_wait_for_activation`
None
#### CMKRESTAPI.`activate`
Activates pending changes

Args:
    sites: On which sites the configuration shall be activated. An empty list means all sites which have pending changes.

Returns:
    (data, etag): usually both empty
#### CMKRESTAPI.`bake_agents`
Bakes agent packages

Returns:
    (data, etag): usually both empty
#### CMKRESTAPI.`set_downtime`
Sets a scheduled downtime on a host or a service

Args:
    comment: string
    start_time: The start datetime of the new downtime. The format has to conform to the ISO 8601 profile 2017-07-21T17:32:28Z
    end_time: The end datetime of the new downtime. The format has to conform to the ISO 8601 profile 2017-07-21T17:42:28Z
    hostname: hostname
    services: if set a list of service descriptions

Returns:
    (data, etag): usually empty
#### CMKRESTAPI.`revoke_downtime`
Revokes scheduled downtime

Args:
    hostname: name of host
    services: list of service descriptions. If empty, all scheduled downtimes for the host will be removed.

Returns:
    (data, etag): usually empty
#### CMKRESTAPI.`create_user`
Creates a new user

Args:
    username: A unique username for the user
    fullname: The alias or full name of the user
    args: additional options (see REST API documentation)

Returns:
    (data, etag): new user object and eTag
#### CMKRESTAPI.`get_user`
Show a user

Args:
    username: Username

Returns:
    (data, etag): user object and eTag
#### CMKRESTAPI.`edit_user`
Edit a user

Args:
    username: The name of the user to edit
    etag: The value of the, to be modified, object's ETag header.
    args: additional options (see REST API documentation)

Returns:
    (data, etag): the user object and eTag
#### CMKRESTAPI.`delete_user`
Delete a user

Args:
    username: The name of the user to delete

Returns:
    Nothing
### checkmkapi.`MultisiteAPI` [class]
None
#### MultisiteAPI.`__init__`
None
#### MultisiteAPI.`_api_request`
None
#### MultisiteAPI.`view`
Fetches data from a Multisite view

Args:
    view_name: name of the view to query
    kwargs: more arguments for the view

Returns:
    List of Dictionaries, every item is a Dict(TableHeader -> Value) for the row
### libthon3.checkmkapi.`_check_mk_url` [function]
adds trailing check_mk path component to URL 
### libthon3.checkmkapi.`_site_url` [function]
None
### libthon3.checkmkapi.`_site_creds` [function]
None
### libthon3.checkmkapi.`CMKRESTAPI` [class]
None
#### CMKRESTAPI.`__init__`
Initialize a REST-API instance. URL, User and Secret can be automatically taken from local site if running as site user.

Args:
    site_url: the site URL
    api_user: username of automation user account
    api_secret: automation secret

Returns:
    instance of CMKRESTAPI
#### CMKRESTAPI.`_check_response`
None
#### CMKRESTAPI.`_get_url`
None
#### CMKRESTAPI.`_post_url`
None
#### CMKRESTAPI.`_put_url`
None
#### CMKRESTAPI.`_delete_url`
None
#### CMKRESTAPI.`add_host`
Adds a host to a folder in the CheckMK configuration.

Args:
    hostname: unique name for the new host
    folder: The folder-id of the folder under which this folder shall be created. May be 'root' for the root-folder.

Returns:
    (data, etag)
    data: host's data
    etag: current etag value
#### CMKRESTAPI.`get_host`
Gets host configuration including eTag value.

Args:
    hostname:  A hostname
    effective_attr: Show all effective attributes, which affect this host, not just the attributes which were set on this host specifically. This includes all attributes of all of this host's parent folders.

Returns:
    (data, etag)
    data: host's data
    etag: current etag value
#### CMKRESTAPI.`get_all_hosts`
Gets all hosts from the CheckMK configuration.

Args:
    effective_attr: Show all effective attributes, which affect this host, not just the attributes which were set on this host specifically. This includes all attributes of all of this host's parent folders.
    attributes: If False do not fetch hosts' data

Returns:
    hosts: Dictionary of host data or dict of hostname -> URL depending on aatributes parameter
#### CMKRESTAPI.`delete_host`
Deletes a host from the CheckMK configuration.

Args:
    hostname: name of the host

Returns:
    (data, etag)
    data: host's data
    etag: current etag value
#### CMKRESTAPI.`edit_host`
Edit a host in the CheckMK configuration.

Args:
    hostname: name of the host
    etag: (optional) etag value, if not provided the host will be looked up first using get_host().
    set_attr: Replace all currently set attributes on the host, with these attributes. Any previously set attributes which are not given here will be removed.
    update_attr: Just update the hosts attributes with these attributes. The previously set attributes will not be touched.
    unset_attr: A list of attributes which should be removed.

Returns:
    (data, etag)
    data: host's data
    etag: current etag value
#### CMKRESTAPI.`disc_host`
Discovers services on a host.

Args:
    hostname: name of the host

Returns:
    (data, etag)
    data: discovery data
    etag: current etag value
#### CMKRESTAPI.`_wait_for_activation`
None
#### CMKRESTAPI.`activate`
Activates pending changes

Args:
    sites: On which sites the configuration shall be activated. An empty list means all sites which have pending changes.

Returns:
    (data, etag): usually both empty
#### CMKRESTAPI.`bake_agents`
Bakes agent packages

Returns:
    (data, etag): usually both empty
#### CMKRESTAPI.`set_downtime`
Sets a scheduled downtime on a host or a service

Args:
    comment: string
    start_time: The start datetime of the new downtime. The format has to conform to the ISO 8601 profile 2017-07-21T17:32:28Z
    end_time: The end datetime of the new downtime. The format has to conform to the ISO 8601 profile 2017-07-21T17:42:28Z
    hostname: hostname
    services: if set a list of service descriptions

Returns:
    (data, etag): usually empty
#### CMKRESTAPI.`revoke_downtime`
Revokes scheduled downtime

Args:
    hostname: name of host
    services: list of service descriptions. If empty, all scheduled downtimes for the host will be removed.

Returns:
    (data, etag): usually empty
#### CMKRESTAPI.`create_user`
Creates a new user

Args:
    username: A unique username for the user
    fullname: The alias or full name of the user
    args: additional options (see REST API documentation)

Returns:
    (data, etag): new user object and eTag
#### CMKRESTAPI.`get_user`
Show a user

Args:
    username: Username

Returns:
    (data, etag): user object and eTag
#### CMKRESTAPI.`edit_user`
Edit a user

Args:
    username: The name of the user to edit
    etag: The value of the, to be modified, object's ETag header.
    args: additional options (see REST API documentation)

Returns:
    (data, etag): the user object and eTag
#### CMKRESTAPI.`delete_user`
Delete a user

Args:
    username: The name of the user to delete

Returns:
    Nothing
### libthon3.checkmkapi.`MultisiteAPI` [class]
None
#### MultisiteAPI.`__init__`
None
#### MultisiteAPI.`_api_request`
None
#### MultisiteAPI.`view`
Fetches data from a Multisite view

Args:
    view_name: name of the view to query
    kwargs: more arguments for the view

Returns:
    List of Dictionaries, every item is a Dict(TableHeader -> Value) for the row
