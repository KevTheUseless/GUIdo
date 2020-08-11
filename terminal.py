class Terminal(TxtField):
	def __init__(self, x, y, w, h):
		self.pwd = '/'
		super().__init__(x, y, w, h, '%s$ ' % self.pwd)
	def pwd(working_dir, args):
		print(working_dir)
	def ls(working_dir, *args):
		files = open("files.img", 'r+')
		lines = files.read().strip('\0').split('\n')
		for i, line in enumerate(lines):
			if line == "!LOC=%s" % working_dir:
				print(lines[i+1].strip('!FNAME='))
	def cat(working_dir, *args):
		if not args:
			print("Missing argument.\nUsage: cat <filename(s)>")
			return
		for target in args:
			files = open("files.img", 'r+')
			lines = files.read().strip('\0').split('\n')
			contents = []
			for i, line in enumerate(lines):
				if line == '!LOC=%s' % working_dir \
				   and lines[i + 1] == '!FNAME=%s' % target:
						for i in range(i+2, len(lines)):
							if lines[i] and lines[i][0] == '!': break
							contents.append(lines[i])
						break
			else:
				print("cat: %s: no such file or directory" % target)
			print('\n'.join(contents))
			files.close()
	def rm(working_dir, *args):
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
	def calc(working_dir, *args):
		expr = input()
		while expr != 'q':
			result = None
			try:
				result = eval(expr)
			except ZeroDivisionError:
				print("Don't divide by zero!")
			except SyntaxError:
				print("Your expression doesn't seem to be valid.")
			except:
				print("This expression doesn't seem to work.")
			if result:
				print(result)
			expr = input()