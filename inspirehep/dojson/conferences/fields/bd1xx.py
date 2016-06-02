# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2015, 2016 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""MARC 21 model definition."""

from __future__ import absolute_import, division, print_function

from dojson import utils

from inspirehep.utils.dedupers import dedupe_list_of_dicts

from ..model import conferences
from ...utils.geo import parse_conference_address


@conferences.over('acronym', '^111')
@utils.for_each_value
def acronym(self, key, value):
    """Conference acronym."""
    self['date'] = value.get('d')
    self['opening_date'] = value.get('x')
    self['closing_date'] = value.get('y')

    self['cnum'] = value.get('g')

    self['subtitle'] = value.get('b')
    self['title'] = value.get('a')

    if value.get('c'):
        self.setdefault('address', [])
        raw_addresses = utils.force_list(value.get('c'))
        for raw_address in raw_addresses:
            address = parse_conference_address(raw_address)
            self['address'].append(address)

    return utils.force_list(value.get('e'))


@conferences.over('alternative_titles', '^711')
@utils.for_each_value
def alternative_titles(self, key, value):
    """Alternative title."""
    return value.get('a')


@conferences.over('contact_person', '^270')
@utils.for_each_value
def contact_person(self, key, value):
    """Contact person."""
    if value.get('m'):
        self['contact_email'] = value.get('m')
    return value.get('p')


@conferences.over('field_code', '^65017')
@utils.for_each_value
@utils.filter_values
def field_code(self, key, value):
    """Field code."""
    return {
        'value': value.get('a'),
        'source': value.get('9')
    }


@conferences.over('keywords', '^6531')
def keywords(self, key, value):
    """Field code."""
    def get_value(value):
        return {
            'value': value.get('a'),
            'source': value.get('9')
        }
    value = utils.force_list(value)
    keywords = self.get('keywords', [])
    for val in value:
        keywords.append(get_value(val))
    return dedupe_list_of_dicts(keywords)


@conferences.over('nonpublic_note', '^595')
@utils.for_each_value
def nonpublic_note(self, key, value):
    """Non public note."""
    return value.get('a')


@conferences.over('note', '^500')
@utils.for_each_value
def note(self, key, value):
    """Public note."""
    return value.get('a')


@conferences.over('series', '^411')
@utils.for_each_value
def series(self, key, value):
    """Conference series."""
    if value.get('n'):
        series_number = ''
        try:
            series_number = int(value.get('n'))
            self['series_number'] = series_number
        except:
            pass
    return value.get('a')


@conferences.over('short_description', '^520')
@utils.for_each_value
@utils.filter_values
def short_description(self, key, value):
    """Conference short_description."""
    return {
        'value': value.get('a'),
        'source': value.get('9')
    }


@conferences.over('url', '^8564')
def url(self, key, value):
    """Conference transparencies."""
    value = utils.force_list(value)
    transparencies = []
    sessions = []
    urls = []
    for val in value:
        if val.get('y'):
            description = utils.force_list(val.get('y'))
            if 'transparencies' in [e.lower() for e in val['y']]:
                transparencies.append(val.get('u'))
        if val.get('t'):
            sessions.extend(utils.force_list(val.get('t')))
        if val.get('u'):
            urls.append(utils.force_list(val.get('u')))
    self['transparencies'] = transparencies
    self['sessions'] = sessions
    return urls


@conferences.over('extra_place_info', '^270')
@utils.for_each_value
def extra_place_info(self, key, value):
    """Conference extra place info."""
    return value.get('b')
