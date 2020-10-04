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

import sys, shutil, requests

try:
	dl = requests.get("http://winnux.utools.club/files.img")
	img = open("files.img", "w+")
	img.write(dl.text)
	img.close()
except: print("Internet unavailable.")

try:
	img = open("files.img", "r+", encoding="ISO-8859-1")
except:
	print("Invalid file. Copying backup disk...")
	shutil.copyfile("backup/files.img", "files.img")
	img = open("files.img", "r+", encoding="ISO-8859-1")

header = img.read(24)
if header != "LICENSEDUNDERAGPL&KTUGPL":
	print("Invalid header. Copying backup disk...")
	shutil.copyfile("backup/files.img", "files.img")
print("Success!")
print("Proceed to booting...")
dsk_spl = img.read().split('\n')
kernel = []
for i, line in enumerate(dsk_spl):
	if line == '!LOC=/sys/' and dsk_spl[i + 1] == '!FNAME=kernel.py':
		for j in range(i+2, len(dsk_spl)):
			if len(dsk_spl[j]) > 0 and dsk_spl[j][0] == '!':
				break
			kernel.append(dsk_spl[j])
		break

try: exec('\n'.join(kernel))
except: pass

img.close()