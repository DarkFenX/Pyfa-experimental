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


from service.data.pyfa_data.command import BaseCommand
from util.repr import make_repr_str


__all__ = [
    'SubsystemAddCommand',
    'SubsystemRemoveCommand',
    'SubsystemClearCommand'
]


class SubsystemAddCommand(BaseCommand):

    def __init__(self, container, subsystem):
        self.__executed = False
        self.container = container
        self.subsystem = subsystem

    def run(self):
        self.container._add_to_set(self.subsystem)
        self.__executed = True

    def reverse(self):
        self.container._remove_from_set(self.subsystem)
        self.__executed = False

    @property
    def executed(self):
        return self.__executed

    def __repr__(self):
        return make_repr_str(self, ())


class SubsystemRemoveCommand(BaseCommand):

    def __init__(self, container, subsystem):
        self.__executed = False
        self.container = container
        self.subsystem = subsystem

    def run(self):
        self.container._remove_from_set(self.subsystem)
        self.__executed = True

    def reverse(self):
        self.container._add_to_set(self.subsystem)
        self.__executed = False

    @property
    def executed(self):
        return self.__executed

    def __repr__(self):
        return make_repr_str(self, ())


class SubsystemClearCommand(BaseCommand):

    def __init__(self, container):
        self.__executed = False
        self.container = container
        self.subsystems = set(container)

    def run(self):
        self.container._clear_set()
        self.__executed = True

    def reverse(self):
        for subsystem in self.subsystems:
            self.container._add_to_set(subsystem)
        self.__executed = False

    @property
    def executed(self):
        return self.__executed

    def __repr__(self):
        return make_repr_str(self, ())
