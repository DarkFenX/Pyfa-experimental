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


from .character import Character
from .fit import Fit
from .pyfadata_mgr import PyfaDataManager


def query_all_fits():
    pyfadata_session = PyfaDataManager.session
    fits = pyfadata_session.query(Fit).all()
    return fits


def query_all_characters():
    pyfadata_session = PyfaDataManager.session
    chars = pyfadata_session.query(Character).all()
    return chars


__all__ = [
    'query_all_fits',
    'query_all_characters'
]
