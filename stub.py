# stub.py
# STUB The Unified Bootloader

import sys

try:
	img = open("files.img", "r")
except:
	print("Invalid file.")
	sys.exit(0)

header = img.read(24)
if header != "LICENSEDUNDERAGPL&KTUGPL":
	print("Invalid file.")
else:
	print("Success!")