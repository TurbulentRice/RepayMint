import numpy as np
from matplotlib import pyplot as plt
from app.loan import Loan
from app.priority_queue import PriorityQueue
from app.method_compare import MethodCompare

# View / plotting module
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
			self.a_func = LoanPlot.plot_queues_analysis
			self.size = len(o.grid)

		elif isinstance(o, PriorityQueue):
			self.p_func = LoanPlot.plot_queue
			self.a_func = LoanPlot.plot_queue_analysis
			self.size = o.size

		elif isinstance(o, Loan):
			self.p_func = LoanPlot.plot_loan
			self.a_func = LoanPlot.plot_loan_analysis
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

	def plot_analysis(self):
		self.a_func(self.loan_obj)

	########################################
	#	"PUBLIC" METHODS
	#	- Accessible without object
	########################################
	# Gets a MethodCompare object, plots each on it's own graph
	@staticmethod
	def plot_queues(mc):
		for queue in mc.grid:
			LoanPlot.plot_queue(queue)

	# Gets a Queue, makes new fig and plots each loan
	@staticmethod
	def plot_queue(queue):
		fig, ax = plt.subplots(num=queue.title)
		for l in queue.Q:
			LoanPlot.plot_loan(l, ax)

	# Gets a Loan, Axes, plots on new Axes if none given
	@staticmethod
	def plot_loan(loan, ax=None):
		if not ax:
			ax = plt.axes()
		x_axis = loan.Payment_History['pay_no']
		y_axis = loan.Payment_History['balance']
		ax.plot(x_axis, y_axis)

	@staticmethod
	def plot_queues_analysis(mc):
		for idx, queue in enumerate(mc.grid):
			LoanPlot.plot_queue_analysis(queue, idx + 1)

	@staticmethod
	def plot_queue_analysis(queue, idx=None):
		# fig, ax = plt.subplots(num=queue.title)
		for i, l in enumerate(queue.Q):
			index = idx if idx is not None else i + 1
			LoanPlot.plot_loan_analysis(l, index)
			
	@staticmethod
	def plot_loan_analysis(loan, idx=None):
		#   Get data we need from Loan object using methods
		history = loan.Payment_History
		payments = loan.pay_no
		highest_bal = float(max(history["balance"]))
		#   PP yields a percentage /100
		#   Convert to current y scale
		pp_over_time = [(history["principal"][i+1] / (history["principal"][i+1]
										+ history["interest"][i+1]) * 100)
										if history["principal"][i+1] != 0
										else 0 for i in range(payments)]
		avg_pp = [sum(pp_over_time[0:i+1]) / (i+1) for i in range(payments)]

		#   Balance History data
		balance_history = [balance for balance in loan.Payment_History["balance"]]
		principal_history = [sum(history["principal"][0:i+1]) for i in range(payments+1)]
		interest_history = [sum(history["interest"][0:i+1]) for i in range(payments+1)]
		total_history = [principal_history[i] + interest_history[i] for i in range(payments+1)]

		####################################
		#   Payment History Plot
		####################################
		title = loan.title if idx is None else f"{loan.title} {idx}"
		plt.figure(title, figsize=(10,7))

		#   Balance History Plots
		#   Define axes of graph based on Highest Balance and # Payments
		balance_graph = plt.subplot(3, 1, 1)
		plt.title("Balance History")
		plt.ylabel("$")
		plt.xlabel("Payment #")
		if highest_bal >= loan.get_total_paid():
			plt.axis([0, payments, 0, highest_bal])
		else:
			plt.axis([0, payments, 0, float(loan.get_total_paid())])
		balance_graph.plot(balance_history, label=f"balance ({loan.start_balance})")
		balance_graph.plot(principal_history, label=f"principal paid ({loan.get_principal_paid()})")
		balance_graph.plot(interest_history, label=f"interest paid ({loan.get_interest_paid()})")
		balance_graph.plot(total_history, label=f"total paid ({loan.get_total_paid()})")
		plt.legend()

		# Monthly Plots
		monthly_graph = plt.subplot(3, 1, 2)
		plt.title("Payment History")
		plt.ylabel("$")
		plt.xlabel("Payment #")

		monthly_graph.bar(history["pay_no"], history["principal"], label="towards principal")
		monthly_graph.bar(history["pay_no"], history["interest"], label="towards interest")
		plt.legend()

		# Principal Efficiency Plots
		# Ddd zeroes to front of percenetages to scale to graph
		pp_over_time.insert(0, 0)
		avg_pp.insert(0, 0)
		interest_graph = plt.subplot(3, 1, 3)
		plt.title("Principal Efficiency")
		plt.ylabel("%")
		plt.xlabel("Payment #")
		# If percentages are 0, display so
		if sum(pp_over_time) == 0:
			plt.axis([0, payments, -1, 1])
		else:
			plt.axis([0, payments, 0, 100])
		interest_graph.plot(pp_over_time, label="% of payment towards principal")
		interest_graph.plot(avg_pp, label="average % towards principal")
		plt.legend()

		# Show
		plt.tight_layout()
		plt.show()
