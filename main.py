# Program that models individual loan ammortization schedules, 
# Compares repayment strategy timelines across multiple Loans,
# Finds best repayment payment strategy based on a goal

from app.view_controller import MainWindow
from app.loan_plot import LoanPlot
from app.loan import Loan, StandardLoan
from app.priority_queue import PriorityQueue
from app.method_compare import MethodCompare
import random

############
#   MAIN
############
if __name__ == "__main__":

	def get_rand_budg():
		return random.uniform(800, 2000)

	def get_rand_loans(n):
		def r_bal():
			return random.uniform(2000, 25000)
		def r_ir():
			return random.uniform(1, 12)
		def r_term():
			return random.randint(12, 360)
		return [StandardLoan(r_bal(), r_ir(), term=r_term()) for i in range(n)]

	##########################################

	# Random example
	my_budget = get_rand_budg()
	my_loans = get_rand_loans(4)

	##########################################

	# Start our primary queue and display
	my_Queue = PriorityQueue(my_loans, my_budget, title="My Loans")
	my_Queue.display_info()

	# Get a new paid-off queue for each repayment mehtod, sort
	avalanche = my_Queue.avalanche().prioritize()
	cascade = my_Queue.cascade().prioritize()
	ice_slide = my_Queue.ice_slide().prioritize()
	blizzard = my_Queue.blizzard().prioritize()
	snowball = my_Queue.snowball().prioritize()

	# Get a PriorityQueue instance from a single loan, paid-off five different ways
	# Compare how each repayment method payed off a single loan

	# single_loan_queue = PriorityQueue([
	# 	avalanche.Q[0], cascade.Q[0], ice_slide.Q[0], blizzard.Q[0], snowball.Q[0]
	# ], my_budget)
	# single_loan_view = LoanPlot(single_loan_queue)
	# single_loan_view.plot_analysis()

	# Get a MethodCompare instance from the paid-off queues, sorted by interest
	# Compare how each repayment method payed off each loan

	# Equivalent to: my_Queue.finish()
	my_MethodCompare = MethodCompare([
		avalanche, cascade, ice_slide, blizzard, snowball
	])
	my_MethodCompare.order_by('interest')
	all_loan_view = LoanPlot(my_MethodCompare)
	all_loan_view.plot_analysis()

	# Show how just the "best" repayment method payed off all the loans
	# best_queue_view = LoanPlot(my_MethodCompare.top())
	# best_queue_view.plot_history()
	# best_queue_view.plot_analysis()

	# GUI/database implemenation
	def launch_GUI():
		#   Amortization Calculator Main Loop
		LoanApp = MainWindow()
		LoanApp.start(StandardLoan(7024.12, 3.75, term=120))

	# launch_GUI()
