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

import argparse
import asyncio

from lsst.ts.IntegrationTests import AuxTelTrackTarget

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t", "--target", required=True, type=str, help="Specify the target to track."
)
args = parser.parse_args()

script_class = AuxTelTrackTarget(target=args.target)

num_scripts = len(script_class.scripts)
print(
    f"\nAuxTel Track Target; running {num_scripts} scripts "
    f"for target configuration:\n{script_class.configs[0]}"
)

asyncio.run(script_class.run())
