#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import itertools


GENERATOR_NAME_INDEX = 1
GENERATOR_INIT_VALUE_INDEX = 4

# Input from Advent of Code's text
DIVISOR = 0x7FFFFFFF  # == 2147483647
generatorsFactor = {'A': 16807, 'B': 48271}
LOWER_BITS = 0xFFFF
# Bits which should be 0 (part 2)
generatorsMultipleBits = {'A': 0x4 - 1, 'B': 0x8 - 1}

SAMPLE_SIZE_1 = int(40e6)
SAMPLE_SIZE_2 = int(5e6)
# Give alive sign after this number of samples
ALIVE_SIZE = int(1e5)


class Generator:
	'''Data and state of a generator'''

	def __init__(self, inputLineList):
		self.name = inputLineList[GENERATOR_NAME_INDEX]
		self.factor = generatorsFactor[self.name]
		self.multipleBits = generatorsMultipleBits[self.name]
		self.value = int(inputLineList[GENERATOR_INIT_VALUE_INDEX])

	def next(self):
		'''Compute next value'''
		self.value = (self.value * self.factor) % DIVISOR

	def nextAcceptable(self):
		'''Compute next acceptable value (for part 2)'''
		self.next()
		while not 0 == (self.value & self.multipleBits):
			self.next()

	def isMatch(self, other):
		'''Check if self and other match'''
		return 0 == (self.value ^ other.value) & LOWER_BITS


def countMatches(input, nextFunc, numSamples):
	'''Count number of matches within numSamples samples applying nextFunc to advance generators'''

	# Make generators
	generators = []
	for genLine in input.inputListsIter():
		generators.append(Generator(genLine))

	# Go through samples
	count = 0
	for i in range(numSamples):
		if (0 == i % ALIVE_SIZE):
			print (i / 1e6, "/", numSamples / 1e6)
		for gen in generators:
			nextFunc(gen)
		if (generators[0].isMatch(generators[1])):
			count += 1
	return count


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 15)

	result1 = countMatches(input, Generator.next, SAMPLE_SIZE_1)
	result2 = countMatches(input, Generator.nextAcceptable, SAMPLE_SIZE_2)

	print ("--------------")
	print ("result1 =", result1)
	print ("result2 =", result2)

