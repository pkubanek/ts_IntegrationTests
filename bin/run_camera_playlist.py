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

from lsst.ts.IntegrationTests import RunCameraPlaylist
from lsst.ts.IntegrationTests.configs.camera_playlist_configs import (
    atcamera_playlists,
    cccamera_playlists,
)

cameras = ["at", "cc"]
playlists = list(set(list(cccamera_playlists.keys()) + list(atcamera_playlists.keys())))
playlists.sort()
playlist_options = []
for item in list(cccamera_playlists.keys()):
    playlist_options.append(("cc", item))
for item in list(atcamera_playlists.keys()):
    playlist_options.append(("at", item))
playlist_options.sort()

parser = argparse.ArgumentParser()
parser.add_argument(
    "camera",
    metavar="camera",
    nargs="?",
    type=str.lower,
    choices=cameras,
    help="Specify which Camera to command (case insensitive).",
)
parser.add_argument(
    "playlist_shortname",
    metavar="playlist_shortname",
    nargs="?",
    type=str.lower,
    choices=playlists,
    help="Specify the playlist short name.",
)
parser.add_argument(
    "-i",
    "--info",
    action="store_true",
    help="Print the allowed options.",
)
args = parser.parse_args()

if not (args.info or args.camera):
    parser.print_help()
    exit()

if args.info:
    print("The allowed options are: ")
    print(*playlist_options, sep="\n")
    exit()

script_class = RunCameraPlaylist(
    camera=args.camera, playlist_shortname=args.playlist_shortname
)

num_scripts = len(script_class.scripts)
print(
    f"\nExecuting the {args.camera.upper()}Camera "
    f"{args.playlist_shortname.capitalize()} playlist."
)

asyncio.run(script_class.run())
