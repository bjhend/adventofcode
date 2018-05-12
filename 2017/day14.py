#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import day10


GRID_SIZE = 128


def hexDigitToBinDigits(hexDigit):
	'''Convert a hex digit to a list of four binary digits'''
	hexNum = int(hexDigit, 16)
	binString = bin(hexNum).lstrip('0b').rjust(4, '0')
	return map(int, list(binString))


def exploreRegion(grid, row, column, regionNum):
	'''Recursively assign regionNum to grid[row][column] and its region'''

	# These are valid indices, but have to be denied nevertheless
	if (row < 0) or (column < 0):
		return

	try:
		# grid[row][column] not part of an already explored region?
		if 1 == grid[row][column]:
			grid[row][column] = regionNum
			exploreRegion(grid, row - 1, column, regionNum)
			exploreRegion(grid, row + 1, column, regionNum)
			exploreRegion(grid, row, column - 1, regionNum)
			exploreRegion(grid, row, column + 1, regionNum)
	except IndexError:
		return


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 14)
	inputText = input.getFirstInputLine()

	# prepare grid
	numUsedSquares = 0
	grid = []
	for row in range(GRID_SIZE):
		rowKey = inputText + '-' + str(row)
		hash = day10.knotHash(rowKey)
		rowDigits = []
		for hexDigit in hash:
			rowDigits += hexDigitToBinDigits(hexDigit)
		numUsedSquares += rowDigits.count(1)
		grid.append(rowDigits)

	print ("result1 =", numUsedSquares)

	numRegions = 0
	for row in range(GRID_SIZE):
		for column in range(GRID_SIZE):
			# Are we in a new region?
			if 1 == grid[row][column]:
				numRegions += 1
				# Use negative region number as new region marker in grid replacing the original 1
				exploreRegion(grid, row, column, -numRegions)

	print ("result2 =", numRegions)



