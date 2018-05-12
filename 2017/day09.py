#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import re


def totalScore(stream):
	# Remove canceled characters
	stream = re.sub(r"!.", "", stream)

	# Handle garbage
	garbageRe = r"<.*?>"
	# Compute garbage size for part 2
	garbageSize = 0
	for m in re.finditer(garbageRe, stream):
		garbageSize += m.end(0) - m.start(0) - 2
	# Remove garbage
	stream = re.sub(garbageRe, "", stream)
	# Remove commas between groups
	stream = re.sub(r",", "", stream)

	# Compute score
	level = 0
	score = 0
	for c in stream:
		if (c == '{'):
			level += 1
			score += level
		elif (c == '}'):
			level -= 1
		else:
			raise Exception()

	return (score, garbageSize)


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 9)

	result1, result2 = totalScore(input.getFirstInputLine())
	print ("result1 =", result1)
	print ("result2 =", result2)


