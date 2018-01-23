#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput


def checksum1(data):
	checksum = 0
	for row in data:
		minVal = min(row)
		maxVal = max(row)
		diff = abs(maxVal - minVal)
		checksum += diff
	return checksum


def checksum2(data):
	checksum = 0
	for row in data:
		for i in range(len(row) - 1):
			first = row[i]
			# iterate over remaining row elements
			for second in row[i+1:]:
				# first divisible by second?
				if 0 == first % second:
					# // is the integer division operator
					checksum += first // second
				elif 0 == second % first:
					checksum += second // first
	return checksum



if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 2, separator='\t', conversion=int)
	data = input.getInputLists()

	print ("checksum1 =", checksum1(data))
	print ("checksum2 =", checksum2(data))


