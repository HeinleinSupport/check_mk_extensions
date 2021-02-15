# Table of Contents

* [checkmkapi](#checkmkapi)
  * [CMKRESTAPI](#checkmkapi.CMKRESTAPI)
    * [\_\_init\_\_](#checkmkapi.CMKRESTAPI.__init__)
    * [add\_host](#checkmkapi.CMKRESTAPI.add_host)
    * [get\_host](#checkmkapi.CMKRESTAPI.get_host)
    * [get\_all\_hosts](#checkmkapi.CMKRESTAPI.get_all_hosts)
    * [delete\_host](#checkmkapi.CMKRESTAPI.delete_host)
    * [edit\_host](#checkmkapi.CMKRESTAPI.edit_host)
    * [disc\_host](#checkmkapi.CMKRESTAPI.disc_host)
    * [activate](#checkmkapi.CMKRESTAPI.activate)
    * [bake\_agents](#checkmkapi.CMKRESTAPI.bake_agents)
    * [set\_downtime](#checkmkapi.CMKRESTAPI.set_downtime)
    * [revoke\_downtime](#checkmkapi.CMKRESTAPI.revoke_downtime)
  * [MultisiteAPI](#checkmkapi.MultisiteAPI)
    * [view](#checkmkapi.MultisiteAPI.view)

<a name="checkmkapi"></a>
# checkmkapi

API-Wrapper for the CheckMK 2.0 REST API and the Multisite API (Views)

<a name="checkmkapi.CMKRESTAPI"></a>
## CMKRESTAPI Objects

```python
class CMKRESTAPI()
```

<a name="checkmkapi.CMKRESTAPI.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(site_url=None, api_user=None, api_secret=None)
```

Initialize a REST-API instance. URL, User and Secret can be automatically taken from local site if running as site user.

**Arguments**:

- `site_url` - the site URL
- `api_user` - username of automation user account
- `api_secret` - automation secret
  

**Returns**:

  instance of CMKRESTAPI

<a name="checkmkapi.CMKRESTAPI.add_host"></a>
#### add\_host

```python
 | add_host(hostname, folder, attributes={})
```

Adds a host to a folder in the CheckMK configuration.

**Arguments**:

- `hostname` - unique name for the new host
- `folder` - The folder-id of the folder under which this folder shall be created. May be 'root' for the root-folder.
  

**Returns**:

  (data, etag)
- `data` - host's data
- `etag` - current etag value

<a name="checkmkapi.CMKRESTAPI.get_host"></a>
#### get\_host

```python
 | get_host(hostname, effective_attr=False)
```

Gets host configuration including eTag value.

**Arguments**:

- `hostname` - A hostname
- `effective_attr` - Show all effective attributes, which affect this host, not just the attributes which were set on this host specifically. This includes all attributes of all of this host's parent folders.
  

**Returns**:

  (data, etag)
- `data` - host's data
- `etag` - current etag value

<a name="checkmkapi.CMKRESTAPI.get_all_hosts"></a>
#### get\_all\_hosts

```python
 | get_all_hosts(effective_attr=False)
```

Gets all hosts from the CheckMK configuration.

**Arguments**:

- `effective_attr` - Show all effective attributes, which affect this host, not just the attributes which were set on this host specifically. This includes all attributes of all of this host's parent folders.
  

**Returns**:

- `hosts` - Dictionary of host data

<a name="checkmkapi.CMKRESTAPI.delete_host"></a>
#### delete\_host

```python
 | delete_host(hostname, etag=None)
```

Deletes a host from the CheckMK configuration.

**Arguments**:

- `hostname` - name of the host
- `etag` - (optional) etag value, if not provided the host will be looked up first using get_host().
  

**Returns**:

  (data, etag)
- `data` - host's data
- `etag` - current etag value

<a name="checkmkapi.CMKRESTAPI.edit_host"></a>
#### edit\_host

```python
 | edit_host(hostname, etag=None, set_attr={}, update_attr={}, unset_attr=[])
```

Edit a host in the CheckMK configuration.

**Arguments**:

- `hostname` - name of the host
- `etag` - (optional) etag value, if not provided the host will be looked up first using get_host().
- `set_attr` - Replace all currently set attributes on the host, with these attributes. Any previously set attributes which are not given here will be removed.
- `update_attr` - Just update the hosts attributes with these attributes. The previously set attributes will not be touched.
- `unset_attr` - A list of attributes which should be removed.
  

**Returns**:

  (data, etag)
- `data` - host's data
- `etag` - current etag value

<a name="checkmkapi.CMKRESTAPI.disc_host"></a>
#### disc\_host

```python
 | disc_host(hostname)
```

Discovers services on a host.

**Arguments**:

- `hostname` - name of the host
  

**Returns**:

  (data, etag)
- `data` - discovery data
- `etag` - current etag value

<a name="checkmkapi.CMKRESTAPI.activate"></a>
#### activate

```python
 | activate(sites=[])
```

Activates pending changes

**Arguments**:

- `sites` - On which sites the configuration shall be activated. An empty list means all sites which have pending changes.
  

**Returns**:

  (data, etag): usually both empty

<a name="checkmkapi.CMKRESTAPI.bake_agents"></a>
#### bake\_agents

```python
 | bake_agents()
```

Bakes agent packages

**Returns**:

  (data, etag): usually both empty

<a name="checkmkapi.CMKRESTAPI.set_downtime"></a>
#### set\_downtime

```python
 | set_downtime(comment, start_time, end_time, hostname, services=None)
```

Sets a scheduled downtime on a host or a service

**Arguments**:

- `comment` - string
- `start_time` - The start datetime of the new downtime. The format has to conform to the ISO 8601 profile 2017-07-21T17:32:28Z
- `end_time` - The end datetime of the new downtime. The format has to conform to the ISO 8601 profile 2017-07-21T17:42:28Z
- `hostname` - hostname
- `services` - if set a list of service descriptions
  

**Returns**:

  (data, etag): usually empty

<a name="checkmkapi.CMKRESTAPI.revoke_downtime"></a>
#### revoke\_downtime

```python
 | revoke_downtime(hostname, services=None)
```

Revokes scheduled downtime

**Arguments**:

- `hostname` - name of host
- `services` - list of service descriptions. If empty, all scheduled downtimes for the host will be removed.
  

**Returns**:

  (data, etag): usually empty

<a name="checkmkapi.MultisiteAPI"></a>
## MultisiteAPI Objects

```python
class MultisiteAPI()
```

<a name="checkmkapi.MultisiteAPI.view"></a>
#### view

```python
 | view(view_name, **kwargs)
```

Fetches data from a Multisite view

**Arguments**:

- `view_name` - name of the view to query
- `kwargs` - more arguments for the view
  

**Returns**:

  List of Dictionaries, every item is a Dict(TableHeader -> Value) for the row

