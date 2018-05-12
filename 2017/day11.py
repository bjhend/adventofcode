#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput


class HexCoordinates:
	'''Coordinates for the hexadecimal grid

	We squeeze the grid to fit into cartesian coordinates. Every
	column of the hex grid is assigned an integer x-coordinate.
	Because neighboring columns are shifted by half a tile in
	north/south direction, the y-ccordinates are either integers
	or half between the integers: Even x columns have integer
	y-coordinates and odd x columns have half-integer y-coordinates.
	'''

	def __init__(self):
		self.x = 0
		self.y = 0

	def go(self, step):
		# If step contains w or e, x-ccordinate changes
		# acccordingly
		if ('w' in step):
			self.x -= 1
		elif ('e' in step):
			self.x += 1

		if (len(step) == 1):
			# A single letter step is pure north or south,
			# so y goes 1 up or down
			dy = 1
		else:
			# We move to the neighboring hex column, so
			# y has to change by 0.5
			dy = 0.5
		# If we are south-bound y decreases, otherwise we are
		# north-bound and y increases
		if ('s' in step):
			dy *= -1
		# Finally update y
		self.y += dy

	def fewestNumSteps(self):
		# Take absolute coordinates, because of rotational symmetry
		absX = abs(self.x)
		absY = abs(self.y)

		# For each column we passed we may gain half a step in
		# north/south direction.
		if (absY <= absX / 2):
			return absX
		else:
			# If that is not sufficient we need to add the remaining
			# steps in north/south direction:
			#    absX + (absY - absX / 2)
			# or short:
			return int(absX / 2 + absY)


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 11, separator=',')

	coords = HexCoordinates()
	maxDist = 0
	for step in input.getInputLists()[0]:
		coords.go(step)
		maxDist = max(maxDist, coords.fewestNumSteps())

	print ("result1 =", coords.fewestNumSteps())
	print ("result2 =", maxDist)


