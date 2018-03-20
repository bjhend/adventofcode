#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017


The main problem of this task is the enormous number of repititions required for
part 2. It is not feasible to just repeat a direct solution of part 1 this many
times.

To solve this we remember that repeating the same reorder operation on a finite
list reproduces the initial order after a finite number of operations, which we
call the cycle length. So we can produce an arbitrary number of repetitions by
only executing the operation that number modulo the cycle length times.

By further investigation we find out that spin and exchange moves operate on the
positions of the programs while the partner move operates on the names of the
programs. This makes the two types independent of each other. The spin and exchange
moves are permutations of the order, so we call them permutation moves.

To find an efficient solution we separate permutation and partner moves entirely
and execute all permutation moves before the partner moves and also determine their
cycle lengths for part two independently.
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import re


SIZE = 16
NUM_CYCLES = 1000000000



class Operation:
	'''Base class for operations on the program line

	The specializations only differ in initialization
	and the apply method. Everything else is common
	and handled in this base class.
	'''

	@staticmethod
	def makeLine():
		'''Make initial line of programs'''
		a = ord('a')
		return [chr(i) for i in range(a, a + SIZE)]

	@staticmethod
	def swap(aList, i, j):
		'''Swap elements at indices i and j in aList'''
		temp = aList[i]
		aList[i] = aList[j]
		aList[j] = temp

	def cycleLen(self):
		'''Compute number of repetitions until operation return original order'''
		oriLine = self.makeLine()
		line = self.makeLine()
		count = 1
		line = self.apply(line)
		while (line != oriLine):
			line = self.apply(line)
			count += 1
		return count

	def multipleApply(self, line, count):
		'''Apply operation multiple times'''

		# This reduces count to the minimal number of operations by
		# removing complete cycles
		count %= self.cycleLen()
		for i in range(count):
			line = self.apply(line)
		return line


class Perm(Operation):
	'''Permutation of positions of the programs'''

	def __init__(self, danceMoves):
		'''Combine permutational moves of danceMoves to a joint permutation'''
		super().__init__()
		def spin(spinCmd):
			'''Do a spin move'''
			m = re.match(r"s(\d+)", spinCmd)
			x = int(m.group(1))
			newPerm = self.perm[-x:] + self.perm[:-x]
			self.perm[:] = newPerm[:]

		def exchange(spinCmd):
			'''Do an exchange move'''
			m = re.match(r"x(\d+)/(\d+)", spinCmd)
			a = int(m.group(1))
			b = int(m.group(2))
			self.swap(self.perm, a, b)

		def doMove(move):
			'''Determine move type and execute it'''
			if 's' == move[0]:
				spin(move)
			elif 'x' == move[0]:
				exchange(move)

		# Init with identical permutation
		self.perm = list(range(SIZE))
		# Apply moves
		for move in danceMoves:
			doMove(move)

	def apply(self, line):
		'''Apply permutation to program line'''
		return [line[i] for i in self.perm]


class PartnerMapping(Operation):
	'''Joint partner moves of all dance moves'''

	def __init__(self, danceMoves):
		'''Combine partner moves of danceMoves to a joint move'''
		super().__init__()
		line = self.makeLine()
		for move in danceMoves:
			if 'p' == move[0]:
				m = re.match(r"p(.)/(.)", move)
				a = m.group(1)
				b = m.group(2)
				self.swap(line, line.index(a), line.index(b))
		self.mapping = dict(zip(self.makeLine(), line))

	def apply(self, line):
		'''Apply partner moves to program line'''
		return [self.mapping[l] for l in line]


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 16, separator=',')
	danceMoves = input.getInputLists()[0]

	perm = Perm(danceMoves)
	partnerMapping = PartnerMapping(danceMoves)

	# Part 1: apply moves once
	letterLine1 = PartnerMapping.makeLine()
	letterLine1 = perm.apply(letterLine1)
	letterLine1 = partnerMapping.apply(letterLine1)
	print("result1 =", ''.join(letterLine1))

	# Part 1: apply moves many times
	letterLine2 = PartnerMapping.makeLine()
	letterLine2 = perm.multipleApply(letterLine2, NUM_CYCLES)
	letterLine2 = partnerMapping.multipleApply(letterLine2, NUM_CYCLES)
	print("result2 =", ''.join(letterLine2))


