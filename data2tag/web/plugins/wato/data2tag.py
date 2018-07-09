#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# ( mode, title, icon, permission, help )

modules += [
    ( "data2tag", _("Data to Tags"), "data2tag", "data2tag",
      _("Configure data to tag synchronisation.")),
]

data2tag_config = "%s/etc/data2tag.conf" % os.environ['OMD_ROOT']

def load_data2tag():
    return store.load_data_from_file(data2tag_config, {}, True)

def mode_data2tag(phase):
    if phase == 'title':
        return _('Data to Tags')

    elif phase == 'buttons':
        global_buttons()
        html.context_button(_('New Config'), folder_preserving_link([('mode', 'edit_data2tag')]), 'new')
        return

    data2tag = load_data2tag()

    if phase == 'action':
        delname = html.var('_delete')
        if delname and html.transaction_valid():
            raise MKUserError(None, 'Deletion not implemented yet. %s not deleted.' % delname)
        return None

    # html.message('<pre>' + pprint.pformat(data2tag) + '</pre>')

    table.begin("data2tag", empty_text = _("There are no configs defined yet."))
    names = data2tag.keys()
    names.sort()
    for name in names:
        table.row()
        edit_url = folder_preserving_link([("mode", "edit_data2tag"), ("edit", name)])
        delete_url = make_action_link([("mode", "data2tag"), ("_delete", name)])
        table.cell(_("Actions"), css="buttons")
        html.icon_button(edit_url, _("Properties"), "edit")
        html.icon_button(delete_url, _("Delete"), "delete")
        table.cell(_("Name"), html.attrencode(name))
    table.end()

def mode_edit_data2tag(phase):
    data2tags = load_data2tag()
    hosttags = load_hosttags()[0] # only tag groups, not aux tags
    name = html.var('edit')
    new = name == None

    tag_elements = []
    for taggroup in hosttags:
        tag_elements.append((taggroup[0], HostTagAttribute(taggroup)))

    # ValueSpec for the TagMap
    vs_tagmap = ListOf(
        Tuple(
            orientation = "horizontal",
            elements = [
                TextAscii(title = _('Column ID')),
                ListOf(
                    Tuple(
                        orientation = "horizontal",
                        elements = [
                            RegExp(RegExp.complete, size = 32, title = _('Regular Expression')),
                            Dictionary(
                                elements = tag_elements,
                                title = _('Tags'),
                            )
                            # HostTagCondition(title = _('Tags'))
                        ]
                    ),
                    title = _('Mapping'),
                )
            ]
        ),
        movable = False,
        add_label = _("Add TagMap"))


    if phase == 'title':
        if new:
            return _('Create new Data to Tag Definition')
        else:
            return _('Edit Data to Tag Definition')

    elif phase == 'buttons':
        html.context_button(_("Data to Tags"), folder_preserving_link([("mode", "data2tag")]), "back")
        return

    if new:
        data2tag = {}
    else:
        data2tag = data2tags.get(name, {})
    
    if phase == 'action':
        if html.transaction_valid():
            tagmap = vs_tagmap.from_html_vars('tagmap')
            # vs_tagmap.validate_value(tagmap, 'tagmap')
            # html.message('<pre>' + pprint.pformat(tagmap) + '</pre>')
            raise MKUserError(None, 'not implemented yet. %s not edited.' % name)
        return

    # html.message('<pre>' + pprint.pformat(data2tag) + '</pre>')
    # html.message('<pre>' + pprint.pformat(hosttags) + '</pre>')
    # html.message('<pre>' + pprint.pformat(globals()) + '</pre>')
    # html.message('<pre>' + pprint.pformat(all_host_attributes()) + '</pre>')

    # configure_attributes(False, {}, 'host_search', parent = None)

    html.begin_form('data2tag', method='POST')
    forms.header(_('Data to Tag Definition'))

    # Name
    forms.section(_('Internal name'), simple = not new)
    if new:
        html.text_input('name')
        html.set_focus('name')
    else:
        html.write_text(name)

    # View
    forms.section(_('View'))
    html.help(_('Specify the view where the data should be from.'))
    html.text_input('view_name', data2tag.get('view_name'))
    if not new:
        html.set_focus('view_name')

    # TagMap
    forms.section(_('TagMap'))
    html.help(_('Define mappings from data in view columns to host tags using regular expressions.'))
    vs_tagmap.render_input('tagmap', data2tag.get('tagmap', []))
        
    forms.end()
    html.button('save', _('Save'))
    html.hidden_fields()
    html.end_form()

modes['data2tag'] = (['data2tag'], mode_data2tag)
modes['edit_data2tag'] = (['data2tag'], mode_edit_data2tag)

config.declare_permission('wato.data2tag', _('Data to Tags'), _('Access to the module <i>Data to Tags</i>'), [ 'admin', ])
