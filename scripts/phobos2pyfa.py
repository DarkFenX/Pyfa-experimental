#===============================================================================
# Copyright (C) 2015 Anton Vorobyov
#
# This file is part of Pyfa 3.
#
# Pyfa 3 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyfa 3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyfa 3. If not, see <http://www.gnu.org/licenses/>.
#===============================================================================


import os
import sys


# Add Pyfa folder to import paths
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..')))


import argparse
import json

import sqlalchemy

import data.eve_data


# Format:
# {JSON file name: (SQLAlchemy entity, {target column name: source field name})}
tables = {
    'dgmattribs': (
        data.eve_data.DgmAttribute,
        {}
    ),
    'dgmeffects': (
        data.eve_data.DgmEffect,
        {}
    ),
    'dgmtypeattribs': (
        data.eve_data.DgmTypeAttribute,
        {}
    ),
    'dgmtypeeffects': (
        data.eve_data.DgmTypeEffect,
        {}
    ),
    'invtypes': (
        data.eve_data.InvType,
        {'typeName': 'typeName_en-us'}
    )
}


def process_table(edb_session, json_path, json_name):
    """
    Handle flow of how JSON is converted into table.
    """
    print('processing {}'.format(json_name))
    table_data = load_table(json_path, json_name)
    write_table(edb_session, json_name, table_data)


def load_table(json_path, json_name):
    """
    Load JSON file related to specified table and return it.
    """
    with open(os.path.join(json_path, '{}.json'.format(json_name))) as f:
        return json.load(f)

def write_table(edb_session, json_name, table_data):
    """
    Generate objects using passed data and add them to database session.
    """
    cls, replacements = tables[json_name]
    # Compose map which will help us to handle differences between SQL Alchemy
    # attribute names and actual SQL column names. Format:
    # {object attribute name: (column, names)}
    alche_map = {}
    for attr in sqlalchemy.inspect(cls).attrs:
        # We're not interested in anything but column descriptors
        if not isinstance(attr, sqlalchemy.orm.ColumnProperty):
            continue
        alche_map[attr.key] = tuple(sorted(c.name for c in attr.columns))
    for row in table_data:
        instance = cls()
        for tgt_attr_name, tgt_column_names in alche_map.items():
            # As SQL Alchemy mapper format implies there might be multiple
            # columns behind single descriptor, go through names for all
            # candidates and check if there's any relevant data in
            # a row (taking replacement map into consideration)
            for tgt_column_name in tgt_column_names:
                src_field_name = replacements.get(tgt_column_name, tgt_column_name)
                if src_field_name in row:
                    setattr(instance, tgt_attr_name, row[src_field_name])
                    break
        edb_session.add(instance)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='This script converts Phobos JSON dump into database usable by pyfa.')
    parser.add_argument('-j', '--json', required=True, type=str, help='The path to Phobos json dump')
    parser.add_argument('-d', '--db', required=True, type=str, help='Path to database')
    args = parser.parse_args()

    # Expand home folder if needed
    json_path = os.path.expanduser(args.json)
    db_path = os.path.expanduser(args.db)

    # Check if there's a file at DB path, and if it's there, remove it
    if os.path.isfile(db_path):
        os.remove(db_path)

    edb_session = data.eve_data.make_evedata_session(db_path)

    for json_name in sorted(tables):
        process_table(edb_session, json_path, json_name)

    print('committing')
    edb_session.commit()