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


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from util.repr import make_repr_str
from .base import EveBase


class EveMarketGroup(EveBase):
    """
    Market Group with all its properties. Directly accessible by pyfa.
    """

    __tablename__ = 'evemarketgroups'

    id = Column('marketGroupID', Integer, primary_key=True)
    name = Column('marketGroupName_en-us', String)

    _parent_id = Column('parentGroupID', Integer, ForeignKey('evemarketgroups.marketGroupID'))
    parent = relationship('EveMarketGroup', backref='children', remote_side=[id])

    def __repr__(self):
        spec = ['id']
        return make_repr_str(self, spec)
