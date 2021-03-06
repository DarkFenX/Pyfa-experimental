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


from unittest.mock import call

from service.data.pyfa_data import *
from tests.model_structure.model_testcase import ModelTestCase


class TestModelSkillProxyAttachedRemove(ModelTestCase):

    def test_do_via_core_switch(self):
        char1 = Character(alias='test char 1')
        char2 = Character(alias='test char 2')
        skill_core = Skill(6, level=3)
        char1.skills.add(skill_core)
        fit = Fit(name='test fit 1')
        fit.character_core = char1
        skill_proxy_removed = next(iter(fit.character_proxy.skills))
        # Action
        econt_calls_before = len(fit._eos_fit.skills.mock_calls)
        fit.character_core = char2
        econt_calls_after = len(fit._eos_fit.skills.mock_calls)
        # Pyfa model
        self.assertEqual(len(fit.character_proxy.skills), 0)
        # Eos model
        self.assertEqual(econt_calls_after - econt_calls_before, 1)
        self.assertEqual(fit._eos_fit.skills.mock_calls[-1], call.remove(skill_proxy_removed._eos_item))
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, False)
        # Reload model via persistence (DB check)
        fit.persist()
        econt_calls_before = len(fit._eos_fit.skills.mock_calls)
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        econt_calls_after = len(fit._eos_fit.skills.mock_calls)
        # Pyfa model
        self.assertEqual(len(fit.character_proxy.skills), 0)
        # Eos model
        self.assertEqual(econt_calls_after - econt_calls_before, 0)

    def test_do_via_core_change(self):
        char = Character(alias='test char 1')
        skill_core = Skill(6, level=3)
        char.skills.add(skill_core)
        fit = Fit(name='test fit 1')
        fit.character_core = char
        skill_proxy_removed = next(iter(fit.character_proxy.skills))
        # Action
        econt_calls_before = len(fit._eos_fit.skills.mock_calls)
        char.skills.remove(skill_core)
        econt_calls_after = len(fit._eos_fit.skills.mock_calls)
        # Pyfa model
        self.assertEqual(len(fit.character_proxy.skills), 0)
        # Eos model
        self.assertEqual(econt_calls_after - econt_calls_before, 1)
        self.assertEqual(fit._eos_fit.skills.mock_calls[-1], call.remove(skill_proxy_removed._eos_item))
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, False)
        # Reload model via persistence (DB check)
        fit.persist()
        econt_calls_before = len(fit._eos_fit.skills.mock_calls)
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        econt_calls_after = len(fit._eos_fit.skills.mock_calls)
        # Pyfa model
        self.assertEqual(len(fit.character_proxy.skills), 0)
        # Eos model
        self.assertEqual(econt_calls_after - econt_calls_before, 0)
