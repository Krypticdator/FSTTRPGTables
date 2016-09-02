from __future__ import print_function

import requests
from db import DBManager


def get_aws_table(name):
    print('fetching table: ' + name)
    response = requests.post(url="https://eo7sjt6hvj.execute-api.us-west-2.amazonaws.com/prod/tables/get",
                             json={"table": name})
    j = response.json()
    print(j)
    table = j['response']
    return table


def save_table_to_db(table):
    db_mgr = DBManager()
    array = []
    for row in table:
        fr = int(row['fr'])
        to = int(row['to'])
        re = row['result']
        ide = row['identifier']
        leads_to = row['leads_to']
        array.append({'identifier': ide, 'fr': fr, 'to': to, 're': re, 'table': row['table_name'],
                      'leads_to_table': leads_to})

    db_mgr.fuzion_tables.add_many((array))
