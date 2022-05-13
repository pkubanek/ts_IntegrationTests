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
from lsst.ts.IntegrationTests.configs.config_registry import registry


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
        self.camera = camera
        self.camera_full = camera.upper() + "Camera"
        playlist_dictionary = getattr(
            playlist_configs, self.camera + "camera_playlists"
        )
        try:
            self.playlist = playlist_dictionary[playlist_shortname]
        except KeyError:
            raise KeyError(
                f"The {self.camera_full} does not have a '{playlist_shortname}' playlist."
            )
        else:
            self.playlist_config = yaml.safe_load(registry["camera_playlist"])
            self.playlist_config["component"] = self.camera_full
            self.playlist_config["parameters"]["playlist"] = self.playlist
            self.configs = (yaml.safe_dump(self.playlist_config),)
