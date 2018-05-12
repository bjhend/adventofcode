#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import re
import copy
import pprint
import itertools
import math



class Component:
	'''Bridge component'''

	class ApplyNotPossible(Exception):
		'''Exception raised when a component cannot be applied'''
		pass

	def __init__(self, line):
		'''Extract component's ports from line'''
		m = re.match(r"(\d+)/(\d+)", line)
		self.ports = [int(m.group(1)), int(m.group(2))]
		self.connectedPort = None
		self.freePort = None

	def isApplied(self):
		'''Check if component is already applied'''
		return self.connectedPort is not None

	def hasPort(self, port):
		'''Check if component has given port'''
		return port in self.ports

	def strength(self):
		'''Return component's strength'''
		return sum(self.ports)

	def apply(self, connectPort):
		'''Try to apply component to given port or raise ApplyNotPossible'''

		# Is component not applicable?
		if self.isApplied() or (not self.hasPort(connectPort)):
			raise self.ApplyNotPossible()

		# Store connected and free port
		self.connectedPort = connectPort
		ports = self.ports.copy()
		ports.remove(connectPort)
		self.freePort = ports.pop()

	def makeFree(self):
		'''Unapply component'''
		self.connectedPort = None
		self.freePort = None


class AllComponents:
	'''Handle all bridge components'''

	def __init__(self, input):
		'''Make list of components given by inpur'''
		self.components = [Component(line) for line in input.inputLineIter()]

	def _iterateSubComponents(self, port, length=0, strength=0):
		'''Recursively apply all free components with given port

		length and strength sum up length and strength of already applied
		components.
		'''
		for component in self.components:
			try:
				# This fails with Component.ApplyNotPossible exception
				# if component was already applied or has wrong ports
				component.apply(port)

				freePort = component.freePort
				# Strength after applying component
				newStrength = strength + component.strength()
				self._iterateSubComponents(freePort, length + 1, newStrength)
				# Make component re-available for other possible bridges
				component.makeFree()

				# Find max strength so far (part 1)
				if newStrength > self.maxStrength:
					self.maxStrength = newStrength
				# Find max strength of so far longest bridge (part 2)
				if length >= self.maxLength:
					self.maxLength = length
					if newStrength > self.maxLengthStrength:
						self.maxLengthStrength = newStrength

			except Component.ApplyNotPossible:
				pass

	def findMaxStrengths(self):
		'''Recurse over all possible bridges'''

		# Init maxima
		self.maxStrength = 0
		self.maxLength = 0
		self.maxLengthStrength = 0

		# We start recursion by applying to port 0
		self._iterateSubComponents(0)
		return self.maxStrength, self.maxLengthStrength



if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 24)

	allComponents= AllComponents(input)
	allComponents.findMaxStrengths()

	print("result1 =", allComponents.maxStrength)
	print("result2 =", allComponents.maxLengthStrength)


