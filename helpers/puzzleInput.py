#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com
'''


import os.path


# Adapt this constant to your preferred default input folder
INPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../input')
# Adapt this constant to change the filename scheme for input files within INPUT_DIR
INPUT_NAME_FORMAT = "{year:04d}/day{day:02d}.txt"   # example: '2017/day07.txt'


class Input:
	'''Read input of a specific day and provide its content in different forms'''

	def __init__(self, year, day, separator=None, conversion=str, inputDir=INPUT_DIR):
		'''Read input and store processing configuration

		separator: split input lines with this separator, None = split at whitespace
		conversion: apply this function to each line or part of a line if separator given
		'''
		self.separator = separator
		self.conversion = conversion
		print ("Retrieving input for year {}, day {}".format(year, day))
		with open(os.path.join(inputDir, INPUT_NAME_FORMAT.format(year=year, day=day))) as inputFile:
			self.input = inputFile.read().rstrip()

	def numInputLines(self):
		'''Return number of input lines'''
		return len(self.getInputLines())

	def rawInputLineIter(self):
		'''Yield input lines without conversion'''
		for line in self.input.split('\n'):
			yield line

	def inputLineIter(self):
		'''Yield input lines after applying conversion to each'''
		for line in self.rawInputLineIter():
			yield self.conversion(line)

	def getInputLines(self):
		'''Get inputLineIter() as list'''
		return [line for line in self.inputLineIter()]

	def getFirstInputLine(self):
		'''Get first input line in case there is only one line'''
		return self.getInputLines()[0]

	def inputListsIter(self):
		'''Split each input line at separators, apply conversion to its parts,
		and yield it as list'''
		for line in self.rawInputLineIter():
			yield [self.conversion(e) for e in line.split(self.separator)]

	def getInputLists(self):
		'''Get inputListsIter() as list'''
		return [lineList for lineList in self.inputListsIter()]


