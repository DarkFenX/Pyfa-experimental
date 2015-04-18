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

from eos import Subsystem as EosSubsystem
from service.data.eve_data.query import query_type, query_attributes
from util.repr import make_repr_str
from .base import PyfaBase


class Subsystem(PyfaBase):
    """
    Pyfa model: ship.{subsystems}
    Eos model: efit.{subsystems}
    DB model: fit.{_subsystems}
    """

    __tablename__ = 'subsystems'

    _id = Column('subsystem_id', Integer, primary_key=True)

    _fit_id = Column('fit_id', Integer, ForeignKey('fits.fit_id'), nullable=False)
    _fit = relationship('Fit', backref=backref(
        '_subsystems', collection_class=set, cascade='all, delete-orphan'))

    _type_id = Column('type_id', Integer, nullable=False)

    def __init__(self, type_id):
        self._type_id = type_id
        self.__generic_init()

    @reconstructor
    def _dbinit(self):
        self.__generic_init()

    def __generic_init(self):
        self.__ship = None
        self._eve_item = None
        self._eos_subsystem = EosSubsystem(self._type_id)

    # Read-only info
    @property
    def eve_id(self):
        return self._type_id

    @property
    def eve_name(self):
        return self._eve_item.name

    @property
    def attributes(self):
        eos_attrs = self._eos_subsystem.attributes
        attr_ids = eos_attrs.keys()
        attrs = query_attributes(self._ship._fit.source.edb, attr_ids)
        attr_map = {}
        for attr in attrs:
            attr_map[attr] = eos_attrs[attr.id]
        return attr_map

    @property
    def effects(self):
        return list(self._eve_item.effects)

    # Auxiliary methods
    @property
    def _ship(self):
        return self.__ship

    @_ship.setter
    def _ship(self, new_ship):
        old_ship = self._ship
        old_fit = getattr(old_ship, '_fit', None)
        new_fit = getattr(new_ship, '_fit', None)
        # Update DB and Eos
        self._unregister_on_fit(old_fit)
        # Update reverse reference
        self.__ship = new_ship
        # Update DB and Eos
        self._register_on_fit(new_fit)
        # Update EVE item
        self._update_source()

    def _register_on_fit(self, fit):
        if fit is not None:
            # Update DB
            # Here we can't set self._fit reference because our cascades
            # are configured to on the parent object, and we have to use
            # fit._subsystems to ensure proper item addition/deletion
            fit._subsystems.add(self)
            # Update Eos
            fit._eos_fit.subsystems.add(self._eos_subsystem)

    def _unregister_on_fit(self, fit):
        if fit is not None:
            # Update DB
            fit._subsystems.remove(self)
            # Update Eos
            fit._eos_fit.subsystems.remove(self._eos_subsystem)

    def _update_source(self):
        try:
            source = self._ship._fit.source
        except AttributeError:
            self._eve_item = None
        else:
            if source is not None:
                self._eve_item = query_type(source.edb, self.eve_id)
            else:
                self._eve_item = None

    def __repr__(self):
        spec = ['eve_id']
        return make_repr_str(self, spec)
