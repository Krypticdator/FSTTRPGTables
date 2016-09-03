# -*- coding: latin-1 -*-
from __future__ import print_function

from traits.api import Int, String, List, HasTraits, Instance, Enum, Button
from traitsui.api import View, HGroup, Item, ListEditor

import utilities
from db import DBManager

all_table_names = utilities.get_all_aws_tablenames()

class TraitsTableOption(HasTraits):
    fr = Int()
    to = Int()
    re = String()
    identifier = String()
    leads_to = String()

    traits_view = View(
        HGroup(
            Item('fr', width=2),
            Item('to', width=2),
            Item('re'),
            Item('identifier'),
            Item('leads_to')
        )
    )


class TraitsTable(HasTraits):
    name = String()
    description = String()
    options = List(Instance(TraitsTableOption, ()))
    upload = Button()

    def load(self, tablename):
        self.name = tablename
        print(tablename)
        db_mgr = DBManager()

        if db_mgr.fuzion_tables.count_options(tablename) > 0:
            pass
        else:
            t = utilities.get_aws_table(tablename)
            utilities.save_table_to_db(t)
        t = db_mgr.fuzion_tables.get_table(tablename)
        for row in t:
            option = TraitsTableOption()
            option.fr = int(row.fr)
            option.to = int(row.to)

            option.re = str(row.re)

            option.identifier = str(row.identifier)
            leads_to = ""
            if row.leads_to_table is not None:
                leads_to = row.leads_to_table
            option.leads_to = leads_to
            self.options.append(option)

    def _upload_fired(self):
        for option in self.options:
            utilities.export_to_aws(name=self.name, identifier=option.identifier, fr=option.fr, to=option.to,
                                    re=option.re, leads_to=option.leads_to)

    view = View(
        Item('name'),
        Item('description'),
        Item('options', editor=ListEditor(style='custom')),
        Item('upload', show_label=False)
    )


class Loader(HasTraits):
    table_to_load = Enum(all_table_names)


if __name__ == '__main__':
    loader = Loader()
    loader.configure_traits()

    table_name = loader.table_to_load

    table = TraitsTable()
    table.load(table_name)

    table.configure_traits()
