# Our "scriptable calculator"
# Calculates an expression
# Enter q to quit

from math import *

def calc(working_dir, args):    # arguments are completely unused
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
