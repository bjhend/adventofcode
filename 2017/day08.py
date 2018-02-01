#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput



class Register:
	'''Class to hold a single register'''

	def __init__(self, name):
		self.name = name
		self.value = 0
		self.max = 0

	def __str__(self):
		return self.name + " -> " + str(self.value)

	def addOffset(self, offset):
		'''Add offset and update max value'''
		self.value += offset
		self.max = max(self.max, self.value)
		return self.value

	def checkCondition(self, comp, value):
		'''Check comparison with given value'''
		return eval(str(self.value) + comp + str(value))


class Memory:
	'''Container for all registers'''

	def __init__(self):
		self.registers = {}

	def getRegister(self, name):
		'''Get a register's value'''
		if (name not in self.registers):
			self.registers[name] = Register(name)
		return self.registers[name]

	def getCurrentMax(self):
		'''Get maximum value of all registers'''
		return max([reg.value for reg in self.registers.values()])

	def getTotalMax(self):
		'''Get all time max of any register'''
		return max([reg.max for reg in self.registers.values()])


class Instruction:
	'''Class for a single instruction'''
	def __init__(self, parts):
		'''Init with parts of code line'''
		instructionSigns = {'inc': 1, 'dec': -1}

		self.var = parts[0]
		sign = instructionSigns[parts[1]]
		self.offset = sign * int(parts[2])
		# parts[3] is always "if"
		self.condVar = parts[4]
		self.comp = parts[5]
		self.condVal = int(parts[6])

	def __str__(self):
		return "{} {} if {} {} {}".format(self.var, self.offset, self.condVar, self.comp, self.condVal)

	def exec(self, memory):
		'''Execute instruction if condition is met'''
		if (self.checkCondition(memory)):
			reg = memory.getRegister(self.var)
			reg.addOffset(self.offset)

	def checkCondition(self, memory):
		'''Check if memory meets condition of this instruction'''
		condReg = memory.getRegister(self.condVar)
		return condReg.checkCondition(self.comp, self.condVal)


class Program:
	'''Container for instructions forming the program'''

	def __init__(self, input):
		self.instructions = [Instruction(parts) for parts in input.inputListsIter()]

	def exec(self):
		'''Execute whole program and return final memory'''
		memory = Memory()
		for instr in self.instructions:
			instr.exec(memory)
		return memory


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 8)

	program = Program(input)
	finalMemory = program.exec()

	print ("result1 =", finalMemory.getCurrentMax())
	print ("result2 =", finalMemory.getTotalMax())

