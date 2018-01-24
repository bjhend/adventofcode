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


def spiralIter():
	'''Generator to produce spiral coordinates'''
	x = 0
	y = 0
	for round in itertools.count(1):
		# Go right to one square above lower right corner of round
		x += 1
		yield x, y
		# Go up until upper right corner
		for i in range(2 * round - 1):
			y += 1
			yield x, y
		# Go left until upper left corner
		for i in range(2 * round):
			x -= 1
			yield x, y
		# Go down until lower left corner
		for i in range(2 * round):
			y -= 1
			yield x, y
		# Go right until lower right corner
		for i in range(2 * round):
			x += 1
			yield x, y


class Data(helpers.infiniteContainers.InfiniteGrid):
	'''Infinite grid to store values'''

	class Finish(Exception):
		'''Exception to announce reached goal'''
		pass

	def __init__(self, limit):
		super().__init__(0)
		self.limit = limit
		self[0][0] = 1

	def setSum(self, x, y):
		'''Store sum of adjacent squares for part 2'''
		sum = 0
		sum += self[x - 1][y - 1]
		sum += self[x - 1][y    ]
		sum += self[x - 1][y + 1]
		sum += self[x    ][y - 1]
		sum += self[x    ][y + 1]
		sum += self[x + 1][y - 1]
		sum += self[x + 1][y    ]
		sum += self[x + 1][y + 1]
		self[x][y] = sum
		if (sum > self.limit):
			raise self.Finish()


def compute1(inputLine):
	'''Compute solution for part 1'''
	count = 1
	for x, y in spiralIter():
		count += 1
		if count == inputLine:
			return abs(x) + abs(y)


def compute2(inputLine):
	'''Compute solution for part 2'''
	try:
		data = Data(inputLine)
		for x, y in spiralIter():
			data.setSum(x, y)
	except Data.Finish:
		return data[x][y]


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 3, conversion=int)
	inputLine = input.getFirstInputLine()

	print ("result1 =", compute1(inputLine))
	print ("result2 =", compute2(inputLine))


