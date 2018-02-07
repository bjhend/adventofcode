#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import re


def makeGraph(input):
	'''Make neighboring graph stored as dictionary with values
	as list of neighbors of keys'''

	graph = {}
	for line in input.inputLineIter():
		# Get all numbers in line
		nodes = [int(m.group(1)) for m in re.finditer(r"(\d+)+", line)]
		# First number is the parent program
		fromNode = nodes.pop(0)
		graph[fromNode] = nodes
	return graph


def allNeighbors(start, neighbors=set()):
	'''Return set of all (direct and indirect) neighbors of start'''

	assert start in graph
	neighbors.add(start)
	for neighbor in graph[start]:
		if (neighbor not in neighbors):
			allNeighbors(neighbor, neighbors)
	return neighbors


if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 12)
	graph = makeGraph(input)

	neighborsOf0 = allNeighbors(0)
	print ("result1 =", len(neighborsOf0))

	groupCount = 0
	remainingPrograms = set(graph.keys())
	while (remainingPrograms):
		# Take any remaining program
		start = remainingPrograms.pop()
		neighbors = allNeighbors(start)
		# Remove neighbors of start from remainingPrograms
		remainingPrograms -= neighbors
		groupCount += 1
	print ("result2 =", groupCount)

