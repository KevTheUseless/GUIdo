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
	exec(img.read().strip('\x00'))

img.close()