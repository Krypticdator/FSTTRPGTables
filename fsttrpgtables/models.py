from __future__ import print_function

from random import randint
from db import DBManager

import utilities


class Table(object):
    def __init__(self, name, load_from_name=True):
        super(Table, self).__init__()
        self.name = name
        self.options = {}
        self.max = 0

        if load_from_name:
            self.load(name)

    def load(self, name):
        db_mgr = DBManager()
        if db_mgr.fuzion_tables.count_options(name) > 0:
            table = db_mgr.fuzion_tables.get_table(name)
            for row in table:
                self.add_option(row.fr, row.to, row.re)
        else:
            table = utilities.get_aws_table(name)
            utilities.save_table_to_db(table)
            table = db_mgr.fuzion_tables.get_table(name)
            for row in table:
                self.add_option(row.fr, row.to, row.re)

    def add_option(self, fr, to, re):
        if fr != to:
            for i in range(fr, to):
                self.options[i] = re
        else:
            self.options[fr] = re
        if to > self.max:
            self.max = to

    def extract_from_array(self, array):
        for row in array:
            self.add_option(row)

    def extract_option_from_json(self, option):
        fr = int(option['fr'])
        to = int(option['to'])
        re = str(option['result'])
        if fr != to:
            for i in range(fr, to):
                self.options[i] = re
        else:
            self.options[fr] = re
        if to > self.max:
            self.max = to

    def results(self):
        results = []
        for key, value in self.options.iteritems():
            if value in results:
                pass
            else:
                results.append(value)
        results.sort()
        return results

    def random_result(self):
        r = randint(1, self.max)
        return self.options[r]

    def multiple_randoms(self, min, max):
        times = randint(min, max)
        # print('times: ' + str(times))
        results = []
        while len(results) < times:
            r = self.random_result()
            if r in results:
                pass
            else:
                results.append(r)
        return results


if __name__ == '__main__':
    pass
