#!/usr/bin/env python
# This file is part of ts_IntegrationTests.
#
# Developed for the Rubin Observatory Telescope and Site System.
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

import asyncio

from lsst.ts import IntegrationTests
from lsst.ts import salobj
from lsst.ts.idl.enums import ScriptQueue


async def amain():
    async with salobj.Domain() as domain, salobj.Remote(
        domain=domain, name="ScriptQueue", index=2
    ) as remote:
        # note: use index=1 for MT, 2 for AuxTel;
        # also since `async with` is used,
        # you do NOT have to wait for the remote to start
        configuration = IntegrationTests.auxtel_visit_config()
        print("Test configuration:\n" + configuration)
        await remote.start_task
        await remote.evt_heartbeat.next(flush=True, timeout=30)
        await remote.cmd_pause.start(timeout=10)
        await remote.cmd_add.set_start(
            timeout=10,
            isStandard=True,
            path="auxtel/take_image_latiss.py",
            config=configuration,
            logLevel=10,
            location=ScriptQueue.Location.FIRST,
        )
        await remote.cmd_resume.set_start(timeout=10)


asyncio.run(amain())
