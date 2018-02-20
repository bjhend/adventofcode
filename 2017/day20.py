#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import re
import itertools
import math


class Vector:
	'''Position, velocity, or acceleration vector'''

	def __init__(self, code):
		'''Parse code for coordinates'''
		m = re.search(r"(-?\d+),(-?\d+),(-?\d+)", code)
		self.coords = [int(m.group(1)), int(m.group(2)), int(m.group(3))]

	def manhattan(self):
		'''Compute Manhattan length'''
		return sum(map(abs, self.coords))

	def __eq__(self, other):
		'''Equality operator'''
		return self.coords == other.coords

	def __lt__(self, other):
		'''Less than operator'''
		return self.manhattan() < other.manhattan()


class Particle:
	'''Container for particle properties'''

	def __init__(self, line):
		m = re.search(r"p=<(.*)>, v=<(.*)>, a=<(.*)>", line)
		self.p = Vector(m.group(1))
		self.v = Vector(m.group(2))
		self.a = Vector(m.group(3))


def findClosest(particles):
	'''Find number of particle which stays closest to origin (part 1)

	In the long run acceleration outplays velocity, which outplays
	position. So search for particle with lowest acceleration and
	among those with lowest velocity and among these with lowest
	position.
	'''

	closest = particles[0]
	for p in particles:
		if p.a < closest.a:
			closest = p
		elif p.a == closest.a:
			if p.v < closest.v:
				closest = p
			elif p.v == closest.v:
				if p.p < closest.p:
					closest = p
	return particles.index(closest)


def coordCollisionTime(p0, p1, coordIndex):
	'''Compute collision times of coordinate number coordIndex of particles p0 and p1

	Returns a frozenset of the points in time these particles would have a matching
	position coordinate provided the time points are integer and in the future.
	'''

	# Diffs of particles' positions, accelerations, and velocities
	dp = p1.p.coords[coordIndex] - p0.p.coords[coordIndex]
	da = p1.a.coords[coordIndex] - p0.a.coords[coordIndex]
	# We need to add da/2, to compensate that a full acc value is added in
	# each round opposed to continuous acceleration here
	dv = p1.v.coords[coordIndex] - p0.v.coords[coordIndex] + da/2

	if 0 == da:
		if 0 == dv:
			if 0 == dp:
				# Initially and forever at the same position
				return frozenset([0])
		else:
			collisionTime = -dp/dv
			if (collisionTime >= 0) and collisionTime.is_integer():
				return frozenset([int(collisionTime)])
	else:
		radicand = (dv * dv) - (2 * dp * da)
		if radicand >= 0:
			sqrt = math.sqrt(radicand)
			collisionTimes = [(-dv + sqrt) / da, (-dv - sqrt) / da]
			return frozenset([int(t) for t in collisionTimes if (t >= 0) and t.is_integer()])
	# No collision of this coordinate
	return frozenset()


def numNonColliding(particles):
	'''Compute number of colliding particles (part 2)'''

	collidingParticles = set()
	# Go through all pairs of particles
	for p0, p1 in itertools.combinations(particles, 2):
		# Make set of equal collision times for all coordinates
		collisionTimes = coordCollisionTime(p0, p1, 0) & coordCollisionTime(p0, p1, 1) & coordCollisionTime(p0, p1, 2)
		if len(collisionTimes) > 0:
			collidingParticles.add(p0)
			collidingParticles.add(p1)
	return len(particles) - len(collidingParticles)



if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 20)

	particles = [Particle(line) for line in input.inputLineIter()]

	print("result1 =", findClosest(particles))
	print("result2 =", numNonColliding(particles))


