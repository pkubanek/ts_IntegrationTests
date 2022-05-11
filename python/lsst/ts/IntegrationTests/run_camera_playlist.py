# This file is part of ts_IntegrationTests
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

__all__ = ["RunCameraPlaylist"]

import yaml
import lsst.ts.IntegrationTests.configs.camera_playlist_configs as playlist_configs

from lsst.ts.IntegrationTests import BaseScript
from .configs.config_registry import registry


class RunCameraPlaylist(BaseScript):
    """Execute the run_command script for the given Playlist,
    for the given Camera, with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index = 2
    configs = ()
    scripts = [
        ("run_command.py", BaseScript.is_standard),
    ]

    def __init__(self, camera, playlist_shortname):
        super().__init__()
        self.camera = camera.upper() + "Camera"
        if self.camera == "ATCamera":
            self.playlist_dictionary = playlist_configs.atcamera_playlists
        else:
            self.playlist_dictionary = playlist_configs.cccamera_playlists
        if playlist_shortname not in self.playlist_dictionary:
            raise Exception(
                f"The {self.camera} does not have a '{playlist_shortname}' playlist."
            )
        self.playlist = self.playlist_dictionary[playlist_shortname]
        self.playlist_config = yaml.safe_load(registry["camera_playlist"])
        self.playlist_config["component"] = self.camera
        self.playlist_config["parameters"]["playlist"] = self.playlist
        self.configs = (yaml.safe_dump(self.playlist_config),)
