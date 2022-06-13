"""Sphinx configuration file for TSSW package"""

from documenteer.conf.pipelinespkg import *


project = "ts-IntegrationTests"
html_theme_options["logotext"] = project  #  type: ignore
html_title = project
html_short_title = project
