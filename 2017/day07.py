#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import re


class Program:
	'''Data of a program'''

	def __init__(self, line):
		'''Parse an input line and provide its program data'''
		m = re.match(r"(\w+)\s*\((\d+)\)", line)
		self.name = m.group(1)
		self.weight = int(m.group(2))

		# Subprograms are either followed by comma or EOL
		self.subprogramsNames = re.findall(r"(\w+)(?:,|$)", line)

	def addSubprograms(self, programsMap):
		'''Add references to subprograms by looking up their names in programsMap'''
		self.subprograms = [programsMap[name] for name in self.subprogramsNames]

	def hasSubprograms(self):
		return len(self.subprogramsNames) > 0

	def totalWeight(self):
		'''Return total weight of self and all its subprograms
		
		The total weight is computed recursively. Because the result will never change
		and the recursion would appear many times we cache the result and return that
		on subsequent calls.
		'''
		try:
			return self._totalWeightCache
		except AttributeError:
			self._totalWeightCache = self.weight + sum(sub.totalWeight() for sub in self.subprograms)
			return self.totalWeight()

	def findUnbalancedSubprogram(self):
		'''Find subprogram which makes self unbalanced or return None'''

		# Map total weights of subprograms on lists of belonging subprograms
		weighs = {}
		for sub in self.subprograms:
			if sub.totalWeight() not in weighs:
				weighs[sub.totalWeight()] = []
			weighs[sub.totalWeight()].append(sub)
		# Do all subprograms have the same total weight?
		if len(weighs) <= 1:
			return None
		# Find subprogram with single total weight and return it
		for sameSubs in weighs.values():
			if len(sameSubs) == 1:
				return sameSubs[0]
		raise Exception("Tree structure not es expected")

	def __str__(self):
		return self.name + " (" + str(self.weight) + ") " + str(self.subprogramsNames)


class Programs:
	'''Container for all programs'''

	def __init__(self, input):
		# Make map of program name to Program object
		self.programs = {}
		for line in input.inputLineIter():
			program = Program(line)
			self.programs[program.name] = program
		# Add refs to subprograms to all programs
		for p in self.programs.values():
			p.addSubprograms(self.programs)

	def bottom(self):
		'''Find bottom program'''

		# Make set of all names of subprograms
		allSubPrograms = set()
		for program in self.programs.values():
			allSubPrograms |= frozenset(program.subprogramsNames)

		# The bottom program is the only program which is not a subprogram as well
		allNames = set(self.programs.keys())
		bottomSet = allNames - allSubPrograms
		assert len(bottomSet) == 1
		# Return the single element in bottomSet
		return bottomSet.pop()



if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 7)

	programs = Programs(input)
	bottomName = programs.bottom()
	print ("result1 =", bottomName)

	##### second part #######

	# Find path of unbalanced programs starting at bottom
	pivot = programs.programs[bottomName]
	unbalancedPath = []
	while pivot:
		unbalancedPath.append(pivot)
		pivot = pivot.findUnbalancedSubprogram()

	# The last program in the path is the culprit with the wrong weight
	wrongWeightProgram = unbalancedPath[-1]
	# The pre-last program is the final unbalanced program
	unbalancedProgram = unbalancedPath[-2]

	# Get any other subprogram of unbalancedProgram
	rightWeightPrograms = set(unbalancedProgram.subprograms)
	rightWeightPrograms.remove(wrongWeightProgram)
	aRightWeightProgram = rightWeightPrograms.pop()

	# Compute and apply correction
	correction = wrongWeightProgram.totalWeight() - aRightWeightProgram.totalWeight()
	result2 = wrongWeightProgram.weight - correction

	print ("result2 =", result2)

