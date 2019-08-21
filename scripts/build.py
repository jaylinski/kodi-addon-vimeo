#!/usr/bin/python

import os
import shutil

src_dir = "."
build_dir = "build"
addon_name = "plugin.video.vimeo"
ignore = shutil.ignore_patterns(".*", "scripts", "tests", "venv", "Pipfile*")

# Clean up
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)

# Copy files
shutil.copytree(".", build_dir + "/" + addon_name, False, ignore)

print("Build finished!")
