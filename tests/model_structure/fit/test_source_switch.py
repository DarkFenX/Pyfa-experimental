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


from service.data.pyfa_data import *
from tests.model_structure.model_testcase import ModelTestCase


class TestModelFitSourceSwitch(ModelTestCase):

    def test_do(self):
        fit = Fit(name='test fit 1', ship=Ship(1))
        # Action
        fit.source = self.source_sisi
        # Pyfa model
        self.assertEqual(fit.name, 'test fit 1')
        self.assertIs(fit.source, self.source_sisi)
        # Eos model
        self.assertIs(fit._eos_fit.source, self.eos_source_sisi)
        # Reload model via persistence (DB check)
        fit.persist()
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        # Pyfa model
        self.assertEqual(fit.name, 'test fit 1')
        # We do not save fit's source into DB
        self.assertIs(fit.source, self.source_tq)
        # Eos model
        self.assertIs(fit._eos_fit.source, self.eos_source_tq)

    def test_undo(self):
        fit = Fit(name='test fit 1', ship=Ship(1))
        fit.source = self.source_sisi
        # Pyfa model
        self.assertIs(fit.source, self.source_sisi)
        # Eos model
        self.assertIs(fit._eos_fit.source, self.eos_source_sisi)
        # Command queues
        self.assertIs(fit.has_undo, True)
        self.assertIs(fit.has_redo, False)
        # Action
        fit.undo()
        # Pyfa model
        self.assertIs(fit.source, self.source_tq)
        # Eos model
        self.assertIs(fit._eos_fit.source, self.eos_source_tq)
        # Command queues
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, True)
        # We do not check persistence because source is not saved into DB

    def test_redo(self):
        fit = Fit(name='test fit 1', ship=Ship(1))
        fit.source = self.source_sisi
        fit.undo()
        # Pyfa model
        self.assertIs(fit.source, self.source_tq)
        # Eos model
        self.assertIs(fit._eos_fit.source, self.eos_source_tq)
        # Command queues
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, True)
        # Action
        fit.redo()
        # Pyfa model
        self.assertIs(fit.source, self.source_sisi)
        # Eos model
        self.assertIs(fit._eos_fit.source, self.eos_source_sisi)
        # Command queues
        self.assertIs(fit.has_undo, True)
        self.assertIs(fit.has_redo, False)
        # We do not check persistence because source is not saved into DB
