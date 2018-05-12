#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import functools
import operator


knotHashSuffix = [17, 31, 73, 47, 23]
knotHashRounds = 64



class String:
	'''String in sense of the task (not string of chars)'''

	def __init__(self, length=256):
		self.string = [x for x in range(length)]
		self.current = 0
		self.skip = 0

	def __str__(self):
		return str(self.string)

	def __len__(self):
		return len(self.string)

	def singleTwist(self, start, size):
		assert size <= len(self)
		end = (start + size) % len(self)
		if (end >= start):
			span = self.string[start:end]
			span.reverse()
			self.string[start:end] = span
		else:
			span = self.string[start:] + self.string[:end]
			span.reverse()
			sizeAtEnd = len(self) - start
			self.string[start:] = span[:sizeAtEnd]
			self.string[:end] = span[sizeAtEnd:]

	def twist(self, twistLengths):
		for i in twistLengths:
			self.singleTwist(self.current, i)
			self.current += (i + self.skip)
			self.current %= len(self)
			self.skip += 1

	def check(self):
		return self.string[0] * self.string[1]

	def denseHash(self):
		result = ""
		for b in range(16):
			start = 16 * b
			end = 16 * (b + 1)
			block = self.string[start:end]
			denseElem = functools.reduce(operator.xor, block)
			result += hex(denseElem).lstrip('0x').rjust(2, '0')
		return result


def knotHash(text):
	lengths = [ord(l) for l in text] + knotHashSuffix
	string = String()
	current = 0
	skip = 0
	for r in range(knotHashRounds):
		string.twist(lengths)
	return string.denseHash()



if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 10, separator=',', conversion=int)

	data = input.getInputLists()[0]
	string = String()
	string.twist(data)
	print ("result1 =", string.check())

	rawInput = list(input.rawInputLineIter())[0]
	print ("result2 =", knotHash(rawInput))


