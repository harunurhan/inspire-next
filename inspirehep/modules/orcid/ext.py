# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
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
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Search extension."""

from __future__ import absolute_import, division, print_function

import inspire_service_orcid.conf


class InspireOrcid(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.init_config(app)
        app.extensions['inspire-orcid'] = self

    def init_config(self, app):
        inspire_service_orcid.conf.settings.configure(
            DO_USE_SANDBOX=False,
            CONSUMER_KEY=app.config['ORCID_APP_CREDENTIALS']['consumer_key'],
            CONSUMER_SECRET=app.config['ORCID_APP_CREDENTIALS']['consumer_secret'],
            REQUEST_TIMEOUT=30,
        )
        # Metrics hooks for inspire_service_orcid are configured in:
        # inspirehep/utils/ext.py::configure_appmetrics
