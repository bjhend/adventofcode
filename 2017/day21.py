#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import re
import copy



class Square:
	'''Single square of pixels'''

	def __init__(self, code=None, rows=None):
		'''Init square either by input code or by giving its rows directly'''

		if code:
			self.rows = []
			mapping = {'.': 0, '#': 1}
			for row in re.findall(r"[.#]+", code):
				self.rows.append([mapping[e] for e in list(row)])
		if rows:
			self.rows = rows

	def size(self):
		return len(self.rows)

	def numPixelsOn(self):
		return sum(map(sum, self.rows))

	def __eq__(self, other):
		return self.rows == other.rows

	def __hash__(self):
		return str(self).__hash__()

	def __str__(self):
		'''Return printable string of square content'''
		mapping = {0: '.', 1: '#'}
		return "\n".join([''.join([mapping[e] for e in r]) for r in self.rows])

	def flip(self):
		'''Flip square vertically'''
		self.rows.reverse()

	def rotate(self):
		'''Rotate square'''
		size = self.size()
		newRows = copy.deepcopy(self.rows)
		for i in range(size):
			for j in range(size):
				newRows[i][j] = self.rows[size - 1 - j][i]
		self.rows = newRows


class Rules:
	'''List of mappings of squares on squares according to rules input'''

	def __init__(self, input):
		def makeRuleVariants(line):
			'''Make all variants of a rule from input'''
			def addRotations():
				'''Add all rotations of squareBefore to rules'''
				for rot in range(4):
					self.rules[copy.deepcopy(squareBefore)] = squareAfter
					squareBefore.rotate()

			addRotations()
			squareBefore.flip()
			addRotations()

		self.rules = {}
		for line in input.inputLineIter():
			m = re.match(r"([.#/]+) => ([.#/]+)", line)
			assert m
			squareBefore = Square(m.group(1))
			squareAfter = Square(m.group(2))
			makeRuleVariants(line)

	def apply(self, square):
		'''Map square on its rule result'''
		assert square in self.rules
		return self.rules[square]


class Grid:
	'''Grid of squares'''

	def __init__(self, rules):
		self.rows = [[Square(".#./..#/###"), ], ]
		self.rules = rules

	def enhance(self):
		'''Apply rules to enhance all squares'''

		for r in range(len(self.rows)):
			for c in range(len(self.rows[r])):
				self.rows[r][c] = self.rules.apply(self.rows[r][c])
		self._split()

	def gridSize(self):
		'''Total size of the grid'''
		squareSize = self.rows[0][0].size()
		return len(self.rows) * squareSize

	def _split(self):
		'''Split the squares into smaller squares if applicable'''

		# Isn't grid divisible by 2?
		if 0 != (self.gridSize() % 2):
			return

		# Make new 2x2 squares
		newRows = []
		squareSize = self.rows[0][0].size()
		for r in range(0, self.gridSize(), 2):
			newRow = []
			# Upper row of new squares
			squareRow0, rowInSquare0 = divmod(r, squareSize)
			squares0 = self.rows[squareRow0]
			# Lower row of new squares
			squareRow1, rowInSquare1 = divmod(r + 1, squareSize)
			squares1 = self.rows[squareRow1]
			for c in range(0, self.gridSize(), 2):
				# Left column of new squares
				squareCol0, colInSquare0 = divmod(c, squareSize)
				# Right column of new squares
				squareCol1, colInSquare1 = divmod(c + 1, squareSize)
				# Make new 2x2 sqaure
				elem00 = squares0[squareCol0].rows[rowInSquare0][colInSquare0]
				elem01 = squares0[squareCol1].rows[rowInSquare0][colInSquare1]
				elem10 = squares1[squareCol0].rows[rowInSquare1][colInSquare0]
				elem11 = squares1[squareCol1].rows[rowInSquare1][colInSquare1]
				newRow.append(Square(rows=[[elem00, elem01], [elem10, elem11]]))
			newRows.append(newRow)
		self.rows = newRows

	def numPixelsOn(self):
		'''Count 'on' pixels in the grid'''
		count = 0
		for r in self.rows:
			for t in r:
				count += t.numPixelsOn()
		return count


def numPixelsOnAfterEnhancements(rules, numEnhancements):
	'''Count number of 'on' pixels after numEnhancements enhancements'''

	grid = Grid(rules)
	for i in range(numEnhancements):
		print("iteration", i + 1)
		grid.enhance()

	return grid.numPixelsOn()


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 21)

	rules = Rules(input)
	result1 = numPixelsOnAfterEnhancements(rules, 5)
	result2 = numPixelsOnAfterEnhancements(rules, 18)

	print("result1 =", result1)
	print("result2 =", result2)


