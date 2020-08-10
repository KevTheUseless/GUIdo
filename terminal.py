from math import *
from kernel import TxtField

class Terminal(TxtField):
	def __init__(self, x, y, w, h):
		self.pwd = '/'
		super().__init__(x, y, w, h, '%s# ' % self.pwd)

	
