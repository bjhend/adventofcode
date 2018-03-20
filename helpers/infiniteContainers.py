#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com

Some containers which grow arbitrarily
'''


import copy
import itertools


class InfiniteList:
	'''List which grows arbitrarily'''

	def __init__(self, default=0):
		self.default = default
		self.data = []

	def __len__(self):
		return len(self.data)

	def __iter__(self):
		return iter(self.data)

	def __contains__(self, item):
		return item in self.data

	def __str__(self):
		return ', '.join(map(str, self.data))

	def _checkIndex(self, i):
		if i >= len(self.data):
			numMissingElements = i - (len(self.data) - 1)
			self.data += [copy.deepcopy(self.default) for j in range(numMissingElements)]

	def __getitem__(self, i):
		self._checkIndex(i)
		return self.data[i]

	def __setitem__(self, i, val):
		self._checkIndex(i)
		self.data[i] = val



class DeInfiniteList:
	'''Double ended InfiniteList: list which grows arbitrarily in positive and negative direction
	'''

	def __init__(self, default=0):
		self.default = default
		self._posArm = InfiniteList(default)
		self._negArm = InfiniteList(default)

	def __len__(self):
		return len(self._negArm) + len(self._posArm)

	def __iter__(self):
		return itertools.chain(reversed(self._negArm), self._posArm)

	def __contains__(self, item):
		return (item in self._negArm) or (item in self._posArm)

	def __str__(self):
		return (', '.join([str(e) for e in reversed(self._negArm)])
	                 + " | " + ', '.join([str(e) for e in self._posArm]))

	def _getArm(self, i):
		if i >= 0:
			return self._posArm, i
		else:
			return self._negArm, -(i + 1)

	def __getitem__(self, i):
		arm, internalIndex = self._getArm(i)
		return arm[internalIndex]

	def __setitem__(self, i, val):
		arm, internalIndex = self._getArm(i)
		arm[internalIndex] = val

	def borders(self):
		return -len(self._negArm), len(self._posArm) - 1


class InfiniteGrid(DeInfiniteList):
	'''2D array growing infinitely in any direction

	If used as an iterator iteration goes through entire
	rows (first index), such that a nested iteration is
	required to go through row elements. This is like
	regular nested lists.
	
	For convenience elementsIter() iterates directly
	through all elements.
	'''

	def __init__(self, default=0):
		super().__init__(DeInfiniteList(default))

	def __contains__(self, item):
		return any(item in row for row in super().__iter__())

	def elementsIter(self):
		"Return an iterator iterating over single elements instead of entire rows"
		for row in self:
			for elem in row:
				yield elem

	def __str__(self):
		return ('\n    '.join([str(e) for e in reversed(self._negArm)])
	                 + "\n------\n    " + '\n    '.join([str(e) for e in self._posArm]))

