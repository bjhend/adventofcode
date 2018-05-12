#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput



class Position:
	'''Position or vector in the diagram'''

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __add__(self, other):
		'''Add other to self Position'''
		return Position(self.x + other.x, self.y + other.y)


class Directions:
	'''Container for posible walk directions'''

	up = Position(0, -1)
	down = Position(0, 1)
	left = Position(-1, 0)
	right = Position(1, 0)

	@staticmethod
	def turnDirections(currDirection):
		'''Return directions orthogonal to currDirection'''

		vertical = (Directions.up, Directions.down)
		horizontal = (Directions.left, Directions.right)
		return horizontal if (currDirection in vertical) else vertical


class Diagram:
	'''Class for storing and walking the diagram'''

	# Symbol classes
	void = ' '
	pureStraight = ['|', '-']
	turn = '+'
	letters = [chr(c) for c in range(ord('A'), ord('Z'))]
	generalStraight = pureStraight + letters

	def __init__(self, input):
		self.rows = [list(l) for l in input.inputLineIter()]

	def get(self, pos):
		'''Get symbol at pos'''
		return self.rows[pos.y][pos.x]

	def findStart(self):
		'''Find start position in first diagram row'''
		for x in range(len(self.rows[0])):
			pos = Position(x, 0)
			if '|' == self.get(pos):
				return pos

	def isValidPos(self, pos):
		'''Check if pos is a valid position in diagram'''
		return ((pos.x >= 0)
		        and (pos.y >= 0)
		        and (pos.y < len(self.rows))
		        and (pos.x < len(self.rows[pos.y])))

	def _newDirection(self):
		'''Helper to determine new direction in case of turn'''
		possibleDirs = Directions.turnDirections(self.currDirection)
		for pd in possibleDirs:
			newPos = self.currPos + pd
			if self.isValidPos(newPos):
				newSymbol = self.get(newPos)
				if newSymbol in self.generalStraight:
					return pd
		assert False

	def walkRoute(self):
		'''Walk the entire diagram route'''

		self.currPos = self.findStart()
		self.currDirection = Directions.down
		pathLetters = []
		numSteps = 0

		while (self.isValidPos(self.currPos)):
			currSymbol = self.get(self.currPos)
			if currSymbol == self.void:
				break
			elif currSymbol in self.pureStraight:
				pass
			elif currSymbol == self.turn:
				self.currDirection = self._newDirection()
			elif currSymbol in self.letters:
				pathLetters.append(currSymbol)
			else:
				assert False
			self.currPos += self.currDirection
			numSteps += 1

		return pathLetters, numSteps


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 19)

	diagram = Diagram(input)
	result1, result2 = diagram.walkRoute()

	print("result1 =", ''.join(result1))
	print("result2 =", result2)


