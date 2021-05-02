# loan-amortization-calculator

Models and plots loan repayment timelines. Compares multi-loan repayment algorithms to determine optimum payment schedule/strategy.

Work in progress! Currently moving plotting functions to loan_plot.py class for clearer modularization,
as well as updating view_controller.py to allow user to interact with PriorityQueue objects in the GUI.

Includes:

- Model-View-Controller structure for main app.
- TKinter GUI, custom Frame class.
- Matplotlib plotting functions.
- MySQL database connection with functions for saving payment histories, running queries, and basic SQL commands.
- Loan data structures for modeling real-world loans.
- PriorityQueue data structure for working with and comparing multiple Loans
- MethodCompare data structure for working with and comparing multiple PriorityQueues

Repayment methods/algorithms modeled in priority_queue.py include Snowball, Avalanche, and custom algorithms Blizzard, Cascade, and Ice Slide.

ALGORITHM METHODS:

---

ORDERED: Focus on targeting a single loan each cycle,
paying only minimums on all except target,
paying one off at a time

---

Avalanche: Order loans by interest rate, balance,
target highest ir until all paid off.
Consistently results in lowest interest paid
over course of large loans.

Blizzard: Order loans by monthly interest cost,
target most expensive until all paid off.
Provides some benefits for small loans,
and/or large budgets

Snowball: Order loans by balance, target loan with
lowest starting bal, pay until all paid off.
Largely motivaitonal, not cost-effective.

---

UNORDERED: Focus on spreading payments strategically, rather
than strict targeting. In the short term, these
methods can reduce monthly cost.

---

Cascade: Unordered, distribute % of budget to each loan
proportional to its % contribution to total
interest rate of all loans.

Ice Slide: Unordered, distribute % of budget to each loan
proportional to its % contribution to total
monthly cost (minimum payments) of all loans.
