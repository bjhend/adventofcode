#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''

import sys
sys.path.append('..')
import helpers.puzzleInput


def captcha(input, dist=1):
	'''Compute captcha with dist as distance between first and second digit'''
	result = 0
	count = len(input)
	for i in range(count):
		first = int(input[i])
		# Get digit dist behind i. Modulo count makes it wrap around.
		second = int(input[int((i + dist) % count)])
		if (first == second):
			result += first
	return result


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 1)
	sequence = input.getFirstInputLine()

	print ("part 1:", captcha(sequence))
	print ("part 2:", captcha(sequence, len(sequence) / 2))

