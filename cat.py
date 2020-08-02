# The `cat` command
# Shows the contents of a given file (in pure text)
# Only works when file is in pwd (for now)

def cat(working_dir, *args):
	if not args:
		print("Missing argument.\nUsage: cat <filename(s)>")
		return
	for target in args:
		files = open("files.img", 'r+')
		lines = files.read().strip('\0').split('\n')
		contents = []
		for i, line in enumerate(lines):
			if line == '!LOC=%s' % working_dir\
		   and lines[i+1] == '!FNAME=%s' % target:
				for i in range(i+2, len(lines)):
					if lines[i] and lines[i][0] == '!': break
					contents.append(lines[i])
				break
		else:
			print("File not found: %s" % target)
		print('\n'.join(contents))
		files.close()
