# Program that models individual loan ammortization schedules, 
# Compares repayment strategy timelines across multiple Loans,
# Finds "best" payment configuration

# Implemenet Model-View-Controller design pattern
# Model:	loan.py, Loan data structures
# View:		loan_plot
# Control:	tk UI

from view_controller import *
from loan_plot import *
from priority_queue import PriorityQueue
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
	#Specific example
	my_budget = 1200
	my_loans = [
		StandardLoan(2406.65, 4.41, title="2014", term=120),
		StandardLoan(2472.91, 3.61, title="2013", term=120)
		#StandardLoan(6282.30, 6.1, title="2012", term=120),
		#StandardLoan(5930.42, 6.1, title="2011", term=120)
		]

	# Random example
	# my_budget = get_rand_budg()
	# my_loans = get_rand_loans(4)

	##########################################

	# Start our primary queue and display
	my_Queue = PriorityQueue(my_loans, my_budget, title="My Loans")

	my_Queue.display_info()

	# Get a new paid-off queue for each repayment mehtod
	# avalanche = my_Queue.avalanche()
	# cascade = my_Queue.cascade()
	# ice_slide = my_Queue.ice_slide()
	# blizzard = my_Queue.blizzard()
	# snowball = my_Queue.snowball()

	# Get a MethodCompare obj of paid off queues sorted by goal
	best = my_Queue.find_best(goal='interest', minimum='int')

	# Display all completed q ordered by "best" method
	print(f'Best:')
	best.display_info(histories=True)


	print(Loan.INSTANCE_COUNTER)

	#JSON Save feature
	c = input("Would you like to save results? (y/n): ")
	if c == 'y':
		for q in best.grid:
			q.save_results()
	else:
		print("Bye!")


	view = LoanPlot(best)
	view.plot_history()


	# GUI/database implemenation
	def launch_GUI():
		#   Amortization Calculator Main Loop
		LoanApp = MainWindow()
		LoanApp.start()

	#launch_GUI()

