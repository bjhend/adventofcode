#!/usr/bin/python3
'''
Author: Björn Hendriks

See http://adventofcode.com/2017
'''


import sys
sys.path.append('..')
import helpers.puzzleInput
import threading



class Registers:
	'''Container for all registers'''

	def __init__(self):
		self._regs= {}

	def get(self, name):
		'''Return register's value or 0 as default'''
		try:
			return self._regs[name]
		except KeyError:
			self._regs[name] = 0
			return self.get(name)

	def set(self, name, value):
		'''Set register value'''
		self._regs[name] = value


class Instruction:
	'''Single instruction from the input'''

	class Value:
		'''Container for a register or literal value passed to an instruction'''

		def __init__(self, registers, arg):
			'''arg may be a literal vaiue or the name of a register'''
			self.registers = registers
			try:
				self.val = int(arg)
			except ValueError:
				self.reg = arg

		def get(self):
			try:
				return self.val
			except AttributeError:
				return self.registers.get(self.reg)

		def getName(self):
			'''Return name in case of a register'''
			return self.reg

	def __init__(self, registers, code, jumpFunc, sndFunc, rcvFunc):
		'''Init instruction with registers container, instruction code, and
		special handlers for jump, snd, and rcv instructions
		'''
		self.registers = registers
		instrs = {
			"snd": self._snd,
			"set": self._set,
			"add": self._add,
			"mul": self._mul,
			"mod": self._mod,
			"rcv": self._rcv,
			"jgz": self._jgz,
			}
		parts = code.split()
		self.name = parts.pop(0)
		self.args = [self.Value(self.registers, p) for p in parts]
		# Method to call on this concrete instruction
		self.func = instrs[self.name]
		# Store special instruction functions
		self.jumpFunc = jumpFunc
		self.sndFunc = sndFunc
		self.rcvFunc = rcvFunc

	def exec(self):
		'''Execute instruction'''
		self.func()

	def _snd(self):
		self.sndFunc(self.args[0].get())

	def _set(self):
		self.registers.set(self.args[0].getName(), self.args[1].get())

	def _add(self):
		self.registers.set(self.args[0].getName(), self.args[0].get() + self.args[1].get())

	def _mul(self):
		self.registers.set(self.args[0].getName(), self.args[0].get() * self.args[1].get())

	def _mod(self):
		self.registers.set(self.args[0].getName(), self.args[0].get() % self.args[1].get())

	def _rcv(self):
		self.rcvFunc(self.args[0])

	def _jgz(self):
		if self.args[0].get() > 0:
			self.jumpFunc(self.args[1].get())


class ProgramBase:
	'''Base class for both programs of part 1 and 2'''

	class Terminate(Exception):
		'''Exception to throw to terminate the program eventually with a result'''
		def __init__(self, result=None):
			self.result = result

	def __init__(self, input):
		self.registers = Registers()
		# self._snd and self._rcv are defined in derived classes
		self.instructions = [Instruction(self.registers, line, self._jump, self._snd, self._rcv)
		                     for line in input.inputLineIter()]

	def _jump(self, offset):
		'''Jump by offset considering the single increment follwing the jump'''
		self.ip += offset - 1

	def exec(self):
		'''Execute program'''

		# instruction pointer
		self.ip = 0
		while True:
			try:
				self.instructions[self.ip].exec()
				self.ip += 1
			except IndexError:
				# ip out of range
				return None
			except self.Terminate as term:
				return term.result


class Program1(ProgramBase):
	'''Specialization of ProgramBase for part 1'''

	def __init__(self, input):
		super().__init__(input)
		self.lastSound = None

	def _snd(self, value):
		self.lastSound = value

	def _rcv(self, valueObject):
		if 0 != valueObject.get():
			raise self.Terminate(self.lastSound)


class Program2Thread(ProgramBase, threading.Thread):
	'''Specialization of ProgramBase for part 2

	This specialization represents a single thread of part 2.
	'''

	def __init__(self, threadId, cond, input):
		'''cond: threading.Condition object to sync threads
		'''
		ProgramBase.__init__(self, input)
		threading.Thread.__init__(self)
		self.cond = cond
		# Init register 'p' with threadId
		self.registers.set("p", threadId)
		with self.cond:
			self.isWaiting = False
			self.rcvQueue = []
		self.sndCount = 0

	def setOtherThread(self, otherThread):
		'''Init ref to other thread'''
		self.otherThread = otherThread

	def run(self):
		'''Thread function executing program'''
		self.exec()

	def _snd(self, value):
		'''Put value into other thread's rcv queue under condition protection'''
		with self.cond:
			self.otherThread.rcvQueue.append(value)
			self.sndCount += 1
			self.cond.notify()

	def _rcv(self, valueObject):
		'''Put next value from rcv queue into valueObject register or detect deadlock'''
		with self.cond:
			self.isWaiting = True
			# Wait until we receive a value or other thread is waiting at an empty rcv queue as well
			while not self.rcvQueue and not (self.otherThread.isWaiting and not self.otherThread.rcvQueue):
				self.cond.wait()
			# Received a value?
			if self.rcvQueue:
				self.isWaiting = False
				self.registers.set(valueObject.getName(), self.rcvQueue.pop(0))
			else:
				# Deadlock, because we and other program are waiting and there's no unprocessed data
				# Let other thread finish as well
				self.cond.notify()
				# Finish this thread
				raise self.Terminate()


class Program2Control:
	'''Handler for both threads of part 2'''

	def __init__(self, input):
		cond = threading.Condition()
		self.thread0 = Program2Thread(0, cond, input)
		self.thread1 = Program2Thread(1, cond, input)
		self.thread0.setOtherThread(self.thread1)
		self.thread1.setOtherThread(self.thread0)

	def exec(self):
		'''Let both threads run until finish and return result'''

		self.thread0.start()
		self.thread1.start()
		self.thread0.join()
		self.thread1.join()

		return self.thread1.sndCount



if __name__ == "__main__":
	input = helpers.puzzleInput.Input(2017, 18)

	# Execute program as defined for part 1
	program1 = Program1(input)
	result1 = program1.exec()

	# Execute program as defined for part 2
	program2 = Program2Control(input)
	result2 = program2.exec()

	print("result1 =", result1)
	print("result2 =", result2)


