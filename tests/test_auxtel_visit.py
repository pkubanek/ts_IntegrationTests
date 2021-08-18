#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of ts_IntegrationTests.
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest
import asyncio

from lsst.ts import salobj


class AuxTelVisitTestCase(unittest.IsolatedAsyncioTestCase):
    # Instantiate the ScriptQueue Controller.
    def default_callback(self, data):
        print(data)

    async def asyncSetUp(self):
        # Set the LSST_DDS_PARTITION_PREFIX ENV_VAR.
        salobj.set_random_lsst_dds_partition_prefix()

        # Create the ScriptQueue Controller and Remote (Commander).
        self.controller = salobj.Controller("ScriptQueue", index=2)

        # Start the controller and wait for it be ready.
        await self.controller.start_task
        self.hb_task = asyncio.create_task(self.pub_hb())

        # Create the Callback mocks for the desired ScriptQueue commands.
        self.controller.cmd_pause.callback = self.default_callback
        self.controller.cmd_add.callback = self.default_callback
        self.controller.cmd_resume.callback = self.default_callback
        # self.controller = IntegrationTests.ScriptQueueController()

    async def pub_hb(self):
        while True:
            self.controller.evt_heartbeat.put()
            await asyncio.sleep(1.0)

    async def test_auxtel_visit(self):
        # Execute the bin/auxtel_visit.py
        script = "auxtel_visit.py"
        child_proccess = await asyncio.create_subprocess_shell(
            script, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await child_proccess.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

        self.assertEqual(child_proccess.returncode, 0)

    async def asyncTearDown(self):
        self.hb_task.cancel()
        await self.controller.close()
