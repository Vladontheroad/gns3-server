# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import aiohttp
import os
import tempfile
from uuid import UUID, uuid4


class Project:
    """
    A project contains a list of VM.
    In theory VM are isolated project/project.

    :param uuid: Force project uuid (None by default auto generate an UUID)
    :param location: Parent path of the project. (None should create a tmp directory)
    """

    def __init__(self, uuid=None, location=None):

        if uuid is None:
            self._uuid = str(uuid4())
        else:
            try:
                UUID(uuid, version=4)
            except ValueError:
                raise aiohttp.web.HTTPBadRequest(text="{} is not a valid UUID".format(uuid))
            self._uuid = uuid

        self._location = location
        if location is None:
            self._location = tempfile.mkdtemp()

        self._path = os.path.join(self._location, self._uuid)
        try:
            os.makedirs(os.path.join(self._path, "vms"), exist_ok=True)
        except OSError as e:
            raise aiohttp.web.HTTPInternalServerError(text="Could not create project directory: {}".format(e))

    @property
    def uuid(self):

        return self._uuid

    @property
    def location(self):

        return self._location

    @property
    def path(self):

        return self._path

    def vm_working_directory(self, module, vm_uuid):
        """
        Return a working directory for a specific VM.
        If the directory doesn't exist, the directory is created.

        :param module: The module name (vpcs, dynamips...)
        :param vm_uuid: VM UUID
        """

        workdir = os.path.join(self._path, module, vm_uuid)
        try:
            os.makedirs(workdir, exist_ok=True)
        except OSError as e:
            raise aiohttp.web.HTTPInternalServerError(text="Could not create VM working directory: {}".format(e))
        return workdir

    def __json__(self):

        return {
            "uuid": self._uuid,
            "location": self._location
        }