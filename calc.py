# Our "scriptable calculator"
# Calculates an expression
# Enter q to quit

from math import *

def calc(working_dir, *args):    # arguments are completely unused
	expr = input()
	while expr != 'q':
		print(eval(expr))
		expr = input()