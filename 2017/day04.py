#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput


class Found(Exception):
	'''Exception raised when an invalid phrase is found'''
	pass

def countInvalidPassphrases(passphrases):
	'''Count number of invalid passphrases'''
	count = 0
	for phrase in passphrases:
		try:
			# go through phrase words
			for i in range(len(phrase) - 1):
				# phrase[i] in remaining phrase words?
				if (phrase[i] in phrase[i + 1:]):
					raise Found
		except Found:
			count += 1
	return count


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 4)

	invalidCount1 = countInvalidPassphrases(input.getInputLists())
	print ("result1 =", input.numInputLines() - invalidCount1)

	# For part 2 we first sort each word in each phrase and then
	# apply the same counting algorithm
	sortedPhrases = []
	for phrase in input.inputListsIter():
		sortedPhrases.append(list(map(sorted, phrase)))
	invalidCount2 = countInvalidPassphrases(sortedPhrases)
	print ("result2 =", input.numInputLines() - invalidCount2)

