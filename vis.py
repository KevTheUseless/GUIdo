# TODO: Rewrite vis file I/O

# vis.py
# Basic CLI text editor

# Accepts text input from user
def write(f):
	# Keeps asking for input
	while True:
		line = input()
		if line == ".":
			f.close()
			break
		line += "\n"
		f.write(line)

# Checks for valid arguments
try:
	filename = sys.argv[1]
except IndexError:
	print("Missing argument.")
	print("Usage: vis <filename>")
	sys.exit(0)

# Main editor loop
while True:
	cmd = input()
	if cmd == "i":
		f = open(sys.argv[1], "w+")
		write(f)
	elif cmd == "a":
		f = open(sys.argv[1], "a+")
		write(f)
	elif cmd == "q":
		sys.exit(0)
	else:
		print("?")
