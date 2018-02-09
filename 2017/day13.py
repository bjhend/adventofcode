#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import re



class Scanner:
	'''Security scanner state'''

	def __init__(self, layer, scannerRange):
		self.layer = layer
		self.range = scannerRange

	def isCatch(self, delay=0):
		'''Return True if scanner would catch packet with given delay'''

		# Number of steps until scanner returns to current position
		repeatSteps = 2 * (self.range - 1)
		# self.layer equals the number of steps until packet reaches
		# this scanner after start, so (delay + self.layer) is the
		# number of steps this scanner has advanced for packet with
		# given delay.
		return 0 == (delay + self.layer) % repeatSteps


class Scanners:
	'''Handles all scanners'''

	def __init__(self, input):
		self.scanners = []
		for line in input.inputLineIter():
			self._addByInputLine(line)

	def _addByInputLine(self, line):
		'''Parse input line and add scanner defined in it'''
		m = re.search(r"(\d+):\s*(\d+)", line)
		layer = int(m.group(1))
		scannerRange = int(m.group(2))
		scanner = Scanner(layer, scannerRange)
		self.scanners.append(scanner)

	def severity(self):
		'''Compute severity of initial state'''
		result = 0
		for s in self.scanners:
			if (s.isCatch()):
				result += s.layer * s.range
		return result

	def isCatch(self, delay):
		'''Return True if packet with given delay would be caught'''
		for s in self.scanners:
			if (s.isCatch(delay)):
				return True
		return False


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 13)

	scanners = Scanners(input)

	print ("result1 =", scanners.severity())

	# Finde delay without packet being caught
	delay = 0
	while (scanners.isCatch(delay)):
		delay += 1
	print ("result2 =", delay)

