#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import day18
import math


class ExtendedInstruction(day18.Instruction):
	'''Extending day18.Instruction with the specialties of today's instruction set

	This code should be an example how to extend an existing class without touching it
	although this extension was not considered in the original day18.Instruction.
	In production code refactoring day18.Instruction should be preferred if ever possible.
	'''

	def __init__(self, registers, code, jumpFunc, notifyMul):
		'''Opposed to day18.Instruction we do not need to handle snd and rcv externally,
		but we need to notify the program if a mul instruction is executed
		'''

		additionalInstrs = {
			"sub": self._sub,
			"jnz": self._jnz,
			}
		# Store function object to notify mul instruction
		self.notifyMul = notifyMul

		# The new instructions raise a KeyError exception in super's __init__ function
		# so we catch that and do the remaining __init__ code here.
		# This is rather fragile code, because a slight change of day18.Instruction.__init__
		# will likely break it.
		try:
			super().__init__(registers, code, jumpFunc, self._noop, self._noop)
		except KeyError:
			self.func = additionalInstrs[self.name]
			# Store special instruction functions
			self.jumpFunc = jumpFunc
			self.sndFunc = self._noop
			self.rcvFunc = self._noop

	def _noop(self, value):
		"Empty handler for snd and rcv instructions"
		pass

	def _sub(self):
		"New sub isntruction"
		self.registers.set(self.args[0].getName(), self.args[0].get() - self.args[1].get())

	def _mul(self):
		"Replacement for original mul instruction notifying the program about it"
		super()._mul()
		self.notifyMul()

	def _jnz(self):
		"New jnz instruction"
		if self.args[0].get() != 0:
			self.jumpFunc(self.args[1].get())


class Program1(day18.ProgramBase):
	'''Specialization of day18.ProgramBase with ExtendedInstructions and counting mul instructions'''

	def __init__(self, input):
		'''To insert our ExtendedInstructions we execute a modified day18.ProgramBase.__init__
		instead of calling it'''

		self.registers = day18.Registers()
		self.instructions = [ExtendedInstruction(self.registers, line, self._jump, self._notifyMul)
		                     for line in input.inputLineIter()]
		self.mulCount = 0

	def _notifyMul(self):
		"Increase mul counter"
		self.mulCount += 1


class Program2:
	'''Program for part 2

	Simply executing the program with the different initial value of register a makes it run way to long.
	To solve this we've manually ported the input code to Python code and simplified it a lot. The result
	is the hand-made code in the exec function.
	'''

	def exec(self):
		'''The input code is a very inefficient algorithm to find and count prime numbers
		in a certain range of candidates. This function does it way more efficient.'''

		# Count how many of every 17th number between 108400 and c is prime
		c = 125400
		h = 0
		# Go through prime candidates
		for b in range(108400, c + 1, 17):
			# Go through possible divisors
			for d in range(2, int(math.sqrt(b)) + 1):
				if 0 == b % d:
					# b is prime
					h += 1
					# try next b
					break
		return h


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 23)

	# Execute program as defined for part 1
	program1 = Program1(input)
	program1.exec()

	# Execute modified program for part 2
	program2 = Program2()
	result2 = program2.exec()

	print("result1 =", program1.mulCount)
	print("result2 =", result2)


