from __future__ import print_function

from traits.api import Int, String, List, HasTraits, Instance, Enum
from traitsui.api import View, HGroup, Item, ListEditor

import utilities
from db import DBManager


class TraitsTableOption(HasTraits):
    fr = Int()
    to = Int()
    re = String()
    identifier = String()

    traits_view = View(
        HGroup(
            Item('fr', width=2),
            Item('to', width=2),
            Item('re')
        )
    )


class TraitsTable(HasTraits):
    name = String()
    description = String()
    options = List(Instance(TraitsTableOption, ()))

    def load(self, tablename):
        self.name = tablename
        print(tablename)
        db_mgr = DBManager()

        if db_mgr.fuzion_tables.count_options(tablename) > 0:
            table = db_mgr.fuzion_tables.get_table(tablename)
            for row in table:
                option = TraitsTableOption()
                option.fr = row.fr
                option.to = row.to
                option.re = row.re
                self.options.append(option)
        else:
            table = utilities.get_aws_table(tablename)
            utilities.save_table_to_db(table)
            table = db_mgr.fuzion_tables.get_table(tablename)
            for row in table:
                option = TraitsTableOption()
                option.fr = row.fr
                option.to = row.to
                option.re = row.re
                self.options.append(option)

    view = View(
        Item('name'),
        Item('description'),
        Item('options', editor=ListEditor(style='custom'))
    )


class Loader(HasTraits):
    table_to_load = Enum('prime_motivations', 'valued_person')


if __name__ == '__main__':
    loader = Loader()
    loader.configure_traits()

    table_name = loader.table_to_load

    table = TraitsTable()
    table.load(table_name)

    table.configure_traits()
