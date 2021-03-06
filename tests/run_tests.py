#!/usr/bin/env python3
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


import os.path
import sys


script_dir = os.path.dirname(os.path.abspath(__file__))
# Add Pyfa paths to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..')))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', 'external')))


import argparse
import unittest

from tests.canned_evedata import make_eve_canneddata


def canned_eve_setup(evedb_path, name):
    make_eve_canneddata(evedb_path, name)


def canned_eve_teardown(evedb_path):
    if os.path.isfile(evedb_path):
        os.remove(evedb_path)


if __name__ == '__main__':

    if sys.version_info.major != 3 or sys.version_info.minor < 3:
        sys.stderr.write('Tests require at least python 3.3 to run\n')
        sys.exit()

    # Parse command line option (which is optional and positional)
    parser = argparse.ArgumentParser(description='Run Pyfa tests')
    parser.add_argument(
        'suite', nargs='?', type=str,
        help='system path to test suite to run, defaults to all tests',
        default=script_dir
    )
    args = parser.parse_args()

    evedb_path_tq = os.path.join(script_dir, '..', 'staticdata',  'canned_tq.db')
    evedb_path_sisi = os.path.join(script_dir, '..', 'staticdata', 'canned_sisi.db')
    canned_eve_setup(evedb_path_tq, name='TQ')
    canned_eve_setup(evedb_path_sisi, name='SiSi')

    # If we have full path to file, adjust pattern so that we execute
    # tests only from that specific file
    suite_path = os.path.expanduser(args.suite)
    if os.path.isfile(suite_path):
        suite, pattern = os.path.split(suite_path)
    else:
        suite = suite_path
        pattern = 'test_*.py'

    # Get all tests into suite
    tests = unittest.TestLoader().discover(suite, pattern=pattern)
    # Run them
    unittest.TextTestRunner().run(tests)

    canned_eve_teardown(evedb_path_tq)
    canned_eve_teardown(evedb_path_sisi)
