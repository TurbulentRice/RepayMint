# View / plotting module

from loan import *
from priority_queue import *

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

# Plots any loan_obj type (Loan, PriorityQueue, list of PriorityQueues)
class LoanPlot:
	def __init__(self, obj):

		# Main object:
		self.loan_obj = obj

		# Private attributes:
		#self.p_func
		#self.size

	################################################
	#	'PRIVATE" PROPERTIES
	#	- Solely for use within object
	#	- Encapsulte these attributes to ensure uniformity
	################################################
	# Main object getter/setter
	# Determines local plotting function (p_func) and size
	@property
	def loan_obj(self):
		return self._loan_obj
	@loan_obj.setter
	def loan_obj(self, o):
		if isinstance(o, MethodCompare):
			self.p_func = LoanPlot.plot_queues
			self.size = len(o.grid)

		elif isinstance(o, PriorityQueue):
			self.p_func = LoanPlot.plot_q
			self.size = o.size

		elif isinstance(o, Loan):
			self.p_func = LoanPlot.plot_l
			self.size = 1

		# Raise error if anyhting other than loan, queue, or list
		else:
			print("Invalid type for LoanPlot.loan_obj")
			raise TypeError

		self._loan_obj = o

	# Local plotting function
	@property
	def p_func(self):
		return self._p_func
	@p_func.setter
	def p_func(self, func):
		self._p_func = func
	
	# Size
	@property
	def size(self):
		return self._size
	@size.setter
	def size(self, s):
		self._size = s

	########################################
	#	"PRIVATE" METHODS
	#	- Main object methods 
	########################################
	# Wrapper for easy plotting using a LoanPlot object
	def plot_history(self):
		self.p_func(self.loan_obj)
		plt.show()

	########################################
	#	"PUBLIC" METHODS
	#	- Accessible without object
	########################################
	# Gets a MethodCompare object, plots each on it's own graph
	@staticmethod
	def plot_queues(mc):
		for q in mc.grid:
			LoanPlot.plot_q(q)

	# Gets a Queue, makes new fig and plots each loan
	@staticmethod
	def plot_q(q):
		fig, ax = plt.subplots(num=q.title)
		for l in q.Q:
			LoanPlot.plot_l(l, ax)

	# Gets a Loan, Axes, plots on new Axes if none given
	@staticmethod
	def plot_l(loan, ax=None):
		if not ax:
			ax = plt.axes()
		x_axis = loan.Payment_History['pay_no']
		y_axis = loan.Payment_History['balance']
		ax.plot(x_axis, y_axis)

	
