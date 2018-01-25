#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput


def countSteps(maze, computeOffsetChange=(lambda jump: 1)):
	'''Count steps until maze is left
	
	computeOffsetChange is a function object which computes
	the change of the offset of the left instruction depending
	on the current jump offset. In part 1 it always returns 1
	(default).
	'''
	count = 0
	i = 0

	# While inside maze
	while ((i >= 0) and (i < len(maze))):
		# Get next jump offset
		jump = maze[i]
		# Change jump offset of current instruction
		maze[i] += computeOffsetChange(jump)
		# Execute the jump
		i += jump
		# Count this step
		count += 1

	return count



if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 5, conversion=int)
	maze = input.getInputLines()

	print ("result1 =", countSteps(input.getInputLines()))

	# computeOffsetChange for part 2 returns 1 or -1 depending
	# if jump is less 3 or not
	computeOffsetChange = lambda jump: 1 if jump < 3 else -1
	print ("result2 =", countSteps(input.getInputLines(), computeOffsetChange))

