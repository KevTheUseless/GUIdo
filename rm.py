# The `rm` command
# Removes a file in pwd (hopefully)

def rm(working_dir, args):
	files = open("files.img", 'r+')
	to_be_written = []
	target = args[0]
	lines = files.read().strip('\0').split('\n')
	write_or_not = True
	for i, line in enumerate(lines):
		if write_or_not:
			if line == '!FNAME=%s' % target\
		   and lines[i-1] == '!LOC=%s' % working_dir:
				write_or_not = False
				del to_be_written[-1]
		else:
			if line and line[0] == '!':
				write_or_not = True
		if write_or_not:
			to_be_written.append(line)
	files.close()
	fw = open("files.img", 'w+')
	fw.write('\n'.join(to_be_written))
	fw.close()
