#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 6, separator='\t', conversion=int)
	blockCounts = input.getInputLists()[0]

	# List of already seen block counts
	results = [blockCounts.copy()]
	size = len(blockCounts)

	def inc(data, inc=1, first=None, last=None):
		"Increment elements of data list between first and last index"
		data[first:last] = [d + inc for d in data[first:last]]

	while (True):
		# Number of blocks to redistribute
		redistBlocks = max(blockCounts)
		# Index of bank with blocks to redistribute
		redistBank = blockCounts.index(redistBlocks)
		blockCounts[redistBank] = 0

		# To make redistribution more efficient we do not
		# distribute one by one. Instead we first compute
		# the number of full redistribution rounds and
		# increase all banks by this number:
		addToAllBanks = redistBlocks // size
		inc(blockCounts, addToAllBanks)

		# Then we compute the remaining number of redistribution
		# blocks:
		remainder = redistBlocks % size
		# Number of banks after the current redistBank
		banksAfter = size - redistBank - 1
		# Compute how many blocks are distributed at the end
		# of the list of banks und how many wrap around to the
		# start:
		if (remainder <= banksAfter):
			atEnd = remainder
			atStart = 0
		else:
			atEnd = banksAfter
			atStart = remainder - banksAfter

		# Increment atEnd blocks after current redistBank
		inc(blockCounts, first=redistBank + 1, last=redistBank + atEnd + 1)
		# Increment atStart blocks at start of banks list
		inc(blockCounts, last=atStart)

		# Are we at a repreated configuration?
		if (blockCounts in results):
			break
		# Store configuration
		results.append(blockCounts.copy())

	print ("result1 =", len(results))

	# Find first appearance of repeated configuration in results
	loopStart = results.index(blockCounts)
	print ("result2 =", len(results) - loopStart)

