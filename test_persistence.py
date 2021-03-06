import os.path
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, 'external')))

import os

from service.data.eve_data.query import *
from service.data.pyfa_data import *
from service.data.pyfa_data.query import *
from service.data.pyfa_data import PyfaDataManager
from service.source import SourceManager

eve_dbpath_tq = os.path.join(script_dir, 'staticdata', 'tranquility.db')
pyfa_dbpath = os.path.join(script_dir, 'userdata', 'pyfadata.db')

# Initialize databases with eve data
SourceManager.add('tq', eve_dbpath_tq, make_default=True)
SourceManager.add('sisi', eve_dbpath_tq)

# (Re-)Initialize database for pyfa save data
PyfaDataManager.set_pyfadb_path(pyfa_dbpath)
session_pyfadata = PyfaDataManager.session


def print_attrs(item):
    print(item.eve_name)
    for k in sorted(item.attributes, key=lambda i: i.name):
        print('  {}: {}'.format(k.name, item.attributes[k]))


for fit in query_all_fits():
    print_attrs(fit.ship)
