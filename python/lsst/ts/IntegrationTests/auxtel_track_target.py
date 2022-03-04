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

__all__ = ["AuxTelTrackTarget"]

import argparse
import yaml

from lsst.ts.IntegrationTests import BaseScript
from .configs.config_registry import registry


class AuxTelTrackTarget(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index = 2
    configs = ()
    scripts = [
        ("auxtel/track_target.py", BaseScript.is_standard),
    ]

    # Add the target argument
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        required=True,
        help="""Specify the target to track.""",
    )

    def __init__(self):
        super().__init__()
        self.parsed = self.parser.parse_args()
        self.target = self.parsed.target
        self.target_config = yaml.safe_load(registry["track_target"])
        self.target_config["target"] = self.target
        self.configs = (self.target_config,)

    def __getattr__(self, name):
        return getattr(self.parsed, name)
