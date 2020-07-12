# stub.py
# STUB The Unified Bootloader

import sys, os

try:
	img = open("files.img", "r")
except:
	print("Invalid file. Copying backup disk...")
	# TODO: Copy backup disk successfully
	# Can't seem to do it...
#	img = open("files.img", "r")

header = img.read(24)
if header != "LICENSEDUNDERAGPL&KTUGPL":
	print("Invalid header. Copying backup disk...")
	# TODO: Copy backup disk successfully
else:
	print("Success!")
	print("Proceed to booting...")
	# TODO: Read kernel from disk