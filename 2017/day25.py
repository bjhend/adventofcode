#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import helpers.infiniteContainers


class Rule:
	'''Rule to apply on a certain state and tape value'''

	# Possible directions to move cursor on tape
	RIGHT = 1
	LEFT = -1

	def __init__(self, writeValue, direction, newState):
		self.writeValue = writeValue
		self.direction = direction
		self.newState = newState


class Tape(helpers.infiniteContainers.DeInfiniteList):
	'''The infinite tape of the turing machine'''

	def __init__(self):
		super().__init__(default=0)
		self.currPos = 0

	def apply(self, rule):
		'''Apply rule to current position'''
		self[self.currPos] = rule.writeValue
		self.currPos += rule.direction

	def currValue(self):
		'''Get value at current position'''
		return self[self.currPos]

	def checksum(self):
		'''Compute checksum'''

		# infiniteContainers.DeInfiniteList is iterable so we can simply sum it
		return sum(self)


class State:
	'''A state of the turing machine'''

	def __init__(self, rule0, rule1):
		'''Init with rules for tape values 0 and 1'''
		self.actions = {0: rule0, 1: rule1}

	def apply(self, tape):
		'''Apply state's rules to tape'''
		rule = self.actions[tape.currValue()]
		tape.apply(rule)
		return rule.newState


class Machine:
	'''The Turing machine'''

	initialState = 'A'

	def __init__(self):
		'''Instead of implementing a parser for the input we manually parsed it into the following states and their rules'''
		self.numSteps = 12523873
		self.states = {
			'A': State( Rule(1, Rule.RIGHT, 'B'), Rule(1, Rule.LEFT , 'E') ),
			'B': State( Rule(1, Rule.RIGHT, 'C'), Rule(1, Rule.RIGHT, 'F') ),
			'C': State( Rule(1, Rule.LEFT , 'D'), Rule(0, Rule.RIGHT, 'B') ),
			'D': State( Rule(1, Rule.RIGHT, 'E'), Rule(0, Rule.LEFT , 'C') ),
			'E': State( Rule(1, Rule.LEFT , 'A'), Rule(0, Rule.RIGHT, 'D') ),
			'F': State( Rule(1, Rule.RIGHT, 'A'), Rule(1, Rule.RIGHT, 'C') ),
			}

	def run(self):
		'''Run the Turing machine the given number of steps and return checksum after that'''
		tape = Tape()
		currState = self.initialState
		for i in range(self.numSteps):
			# Give notification every 100000 steps
			if 0 == i % 100000:
				print(i, "/", self.numSteps)
			currState = self.states[currState].apply(tape)
		return tape.checksum()



if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 25)

	machine = Machine()
	result1 = machine.run()
	print("result1 =", result1)

	# This day has no part 2
	#print("result2 =")

