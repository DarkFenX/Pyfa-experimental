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


from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref, reconstructor

from eos import ModuleHigh as EosModuleHigh, ModuleMed as EosModuleMed, ModuleLow as EosModuleLow
from service.data.pyfa_data.base import PyfaBase, EveItemWrapper
from util.const import RackType
from util.repr import make_repr_str


eos_rack_map = {
    RackType.high: 'high',
    RackType.med: 'med',
    RackType.low: 'low'
}

eos_item_map = {
    RackType.high: EosModuleHigh,
    RackType.med: EosModuleMed,
    RackType.low: EosModuleLow
}


class Module(PyfaBase, EveItemWrapper):
    """
    Pyfa model: fit.modules.[high]/[med]/[low]
    Eos model: efit.modules.[high]/[med]/[low]
    DB model: fit.{_db_modules}
    """

    __tablename__ = 'modules'

    _db_id = Column('subsystem_id', Integer, primary_key=True)

    _db_fit_id = Column('fit_id', Integer, ForeignKey('fits.fit_id'), nullable=False)
    _db_fit = relationship('Fit', backref=backref(
        '_db_modules', collection_class=set, cascade='all, delete-orphan'))

    _db_type_id = Column('type_id', Integer, nullable=False)
    _db_rack_id = Column('rack_id', Integer, nullable=False)
    _db_index = Column('index', Integer, nullable=False)

    def __init__(self, type_id):
        self._db_type_id = type_id
        self.__generic_init()

    @reconstructor
    def _dbinit(self):
        self.__generic_init()

    def __generic_init(self):
        EveItemWrapper.__init__(self, self._db_type_id)
        self.__parent_ship = None
        self.__eos_module = None

    # EVE item wrapper methods
    @property
    def _source(self):
        try:
            return self._parent_ship._parent_fit.source
        except AttributeError:
            return None

    @property
    def _eos_item(self):
        return self.__eos_module

    # Auxiliary methods
    def _set_position(self, rack, index):
        # As we have single module type which fits into all racks in pyfa
        # and specific classes in eos, we have to take care of situation
        # where module changes its racks - thus we need to re-initiate all
        # eos module objects on pyfa module addition to/removal from rack
        if self._db_rack_id != rack:
            try:
                eos_class = eos_item_map[rack]
            except KeyError:
                self.__eos_module = None
            # TODO: initialize more stuff here, like states, charges, etc
            else:
                self.__eos_module = eos_class(self._db_type_id)
            self._db_rack_id = rack
        self._db_index = index

    @property
    def _parent_ship(self):
        return self.__parent_ship

    @_parent_ship.setter
    def _parent_ship(self, new_ship):
        old_ship = self._parent_ship
        old_fit = getattr(old_ship, '_parent_fit', None)
        new_fit = getattr(new_ship, '_parent_fit', None)
        # Update DB and Eos
        self._unregister_on_fit(old_fit)
        # Update parent reference
        self.__parent_ship = new_ship
        # Update DB and Eos
        self._register_on_fit(new_fit)
        # Update EVE item
        self._update_source()

    def _register_on_fit(self, fit):
        if fit is not None:
            # Update DB
            fit._db_modules.add(self)
            # Update Eos
            eos_rack = self.__get_eos_rack(fit)
            eos_rack.place(self._db_index, self._eos_item)

    def _unregister_on_fit(self, fit):
        if fit is not None:
            # Update DB
            fit._db_modules.remove(self)
            # Update Eos
            eos_rack = self.__get_eos_rack(fit)
            eos_rack.free(self._eos_item)

    def __get_eos_rack(self, fit):
        return getattr(fit._eos_fit.modules, eos_rack_map[self._db_rack_id])

    def __repr__(self):
        spec = ['eve_id']
        return make_repr_str(self, spec)
