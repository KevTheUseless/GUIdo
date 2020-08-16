# vis.py
# Basic CLI text editor

def vis(working_dir, *args):
	if not args:
		print("Missing argument. Usage: vis <filename>", end='\r')
	while True:
		cmd = input()
		if cmd == "i":
			rm(working_dir, args[0])
			files = open("files.img", 'r+')
			output = io.StringIO()
			with redirect_stdout(output):
				print("!FNAME=" + args[0])
				print("!LOC=" + working_dir)
				while True:
					line = input()
					line += '\r'
					if line == ".":
						break
			files.write(output.getvalue())
			files.close()
		elif cmd == "a":
			files = open("files.img", 'r+')
			lines = files.read().strip('\0').split('\n')
			contents = []
			for i, line in enumerate(lines):
				if line == '!LOC=%s' % working_dir \
				   and lines[i + 1] == '!FNAME=%s' % args[0]:
						for i in range(i + 2, len(lines)):
							if lines[i] and lines[i][0] == '!': break
							contents.append(lines[i])
						break
			else:
				files = open("files.img", 'r+')
				output = io.StringIO()
				with redirect_stdout(output):
					print("!FNAME=" + args[0])
					print("!LOC=" + working_dir)
					while True:
						line = input()
						line += '\r'
						if line == ".":
							break
				files.write(output.getvalue())
				break
			files.close()
		elif cmd == "q":
			return
		else:
			print("?", end='\r')