#
# OS emulator using pygame.
# Copyright (C) 2020 The-UltimateGamer & pythonleo
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# stub.py
# STUB The Unified Bootloader

import sys, shutil

try:
	img = open("files.img", "r+")
except:
	print("Invalid file. Copying backup disk...")
	shutil.copyfile("backup/files.img", "files.img")
	img = open("files.img", "r+")

header = img.read(24)
if header != "LICENSEDUNDERAGPL&KTUGPL":
	print("Invalid header. Copying backup disk...")
	shutil.copyfile("backup/files.img", "files.img")
else:
	print("Success!")
	print("Proceed to booting...")
	exec(img.read().strip('\0'))

img.close()