#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import helpers.infiniteContainers
import itertools
import copy

# Possible node states
CLEAN = '.'
INFECTED = '#'
# Additional states for part 2
WEAKENED = "W"
FLAGGED = "F"


class Carrier:
	'''Virus Carrier'''

	def __init__(self, inputIter, transitions):
		'''Init Carrier with initial node states (input) and state transitions
		
		A transition maps a current state on a turn direction and a new state.
		'''

		# Infinite grid of notes with default state CLEAN
		self.grid = helpers.infiniteContainers.InfiniteGrid(CLEAN)
		for y, line in zip(itertools.count(), inputIter):
			for x, node in zip(itertools.count(), line):
				self.grid[x][y] = node
		# Start at the center
		self.currX = x // 2
		self.currY = y // 2
		# Possible directions clockwise
		self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
		self.currDirIdx = 0
		self.transitions = transitions
		self.infectionCount = 0

	def multipleBursts(self, numBursts, numBurstsAliveMsg=None):
		'''Do multiple bursts in a row and eventually give alive messages every numBurstsAliveMsg burst'''
		for i in range(numBursts):
			if numBurstsAliveMsg and (0 == i % numBurstsAliveMsg):
				print (i)
			self.burst()

	def _turn(self, dir):
		'''Turn none, right, left, or reverse'''
		turnOffset = {"none": 0, "right": 1, "left": -1, "reverse": 2}
		self.currDirIdx = (self.currDirIdx + turnOffset[dir]) % len(self.directions)

	def _moveForward(self):
		'''Move to the next node in current direction'''
		self.currX += self.directions[self.currDirIdx][0]
		self.currY += self.directions[self.currDirIdx][1]

	def burst(self):
		'''Perform a single burst'''
		currState = self.grid[self.currX][self.currY]
		turnDir, newState = self.transitions[currState]
		self._turn(turnDir)
		self.grid[self.currX][self.currY] = newState
		if INFECTED == newState:
			self.infectionCount += 1
		self._moveForward()



if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 22)

	# Part 1
	transitions1 = {
		INFECTED: ("right", CLEAN   ),
		CLEAN:    ("left" , INFECTED),
	}
	carrier1 = Carrier(input.inputLineIter(), transitions1)
	carrier1.multipleBursts(10000)

	# Part 2
	transitions2 = {
		CLEAN:    ("left"   , WEAKENED),
		INFECTED: ("right"  , FLAGGED ),
		FLAGGED:  ("reverse", CLEAN   ),
		WEAKENED: ("none"   , INFECTED),
	}
	carrier2 = Carrier(input.inputLineIter(), transitions2)
	carrier2.multipleBursts(10000000, 100000)

	# Results
	print("result1 =", carrier1.infectionCount)
	print("result2 =", carrier2.infectionCount)


