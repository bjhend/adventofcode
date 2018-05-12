#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput

numInsertions1 = 2017
numInsertions2 = 50000000


def getResult1(inputValue):
	'''Compute result for part 1'''

	def advanceCurrPos(offset=1):
		return (currPos + offset) % len(buffer)

	buffer = [0]
	currPos = 0
	for i in range(1, numInsertions1 + 1):
		currPos = advanceCurrPos(inputValue) + 1
		buffer.insert(currPos, i)
	return buffer[advanceCurrPos()]


def getResult2(inputValue):
	'''Compute result for part 1

	In this case we do not need to store the entire buffer (which
	would not be feasible anyway). We're only interested in the
	value at position 1, which we store as result2.
	'''

	lenBuffer = 1
	currPos = 0
	for i in range(1, numInsertions2 + 1):
		currPos = ((currPos + inputValue) % lenBuffer) + 1
		lenBuffer += 1
		if 1 == currPos:
			result2 = i
	return result2


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 17, conversion=int)
	inputValue = input.getFirstInputLine()

	print("result1 =", getResult1(inputValue))
	print("result2 =", getResult2(inputValue))


