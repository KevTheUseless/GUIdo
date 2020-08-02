# The `ls` command
# Shows all files in pwd

def ls(working_dir, *args):
	files = open("files.img", 'r+')
	lines = files.read().strip('\0').split('\n')
	for i, line in enumerate(lines):
		if line == "!LOC=%s" % working_dir:
			print(lines[i+1].strip('!FNAME='))
