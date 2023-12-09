#   Data structures for ordering Loans and testing repayment methods
#   Receives list of StandardLoans and a monthly budget

from app.loan import Loan
from app.method_compare import MethodCompare

#########################################
#   LOAN PRIORITY QUEUE
#########################################

class PriorityQueue:
    def __init__(self, loans: [Loan], budget: float=None, title=None):

        # Primary attributes
        self.title = title
        self.Q = loans
        self.budget = budget

    ##################################
    #   PRIMARY GETTER / SETTERS
    ##################################
    # Title
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, t):
        if t is None:
            self._title = "My Queue"
        else:
            self._title = t
    # Budget
    @property
    def budget(self):
        return self._budget if self._budget is not None else Loan.Dec(sum([loan.payment_amt for loan in self.Q]))
    @budget.setter
    def budget(self, b):
        self._budget = Loan.Dec(b) if b is not None else b

    # Length of Q
    @property
    def size(self):
        return len(self.Q)
    
    def to_json(self):
        return [loan.to_json() for loan in self.Q]

    ##################################
    #   EVALUATIVE METHODS
    ##################################
    def is_complete(self):
        return all([l.is_complete() for l in self.Q])

    def get_duration(self):
        return max([l.pay_no for l in self.Q])

    def get_num_payments(self):
        return sum([l.pay_no for l in self.Q])

    def get_principal_paid(self):
        return sum([l.get_principal_paid() for l in self.Q])

    def get_interest_paid(self):
        return sum([l.get_interest_paid() for l in self.Q])

    def get_total_paid(self):
        return sum([l.get_total_paid() for l in self.Q])

    def get_avg_p_to_i(self):
        return Loan.Dec(sum([l.get_p_to_i() for l in self.Q])/self.size)

    def get_percent_principal(self):
        return Loan.Dec(self.get_principal_paid() / self.get_total_paid() * 100)
    
    def get_analysis(self):
        return {
            "duration": self.get_duration(),
            "num_payments": self.get_num_payments(),
            "principal_paid": self.get_principal_paid(),
            "interest_paid": self.get_interest_paid(),
            "total_paid": self.get_total_paid(),
            'avg_pi': self.get_avg_p_to_i(),
            "percent_principal": self.get_percent_principal()
        }

    ##############################
    #   PREPARATION METHODS
    ##############################
    # Takes one or a list of Loans to append
    def add_loan(self, new):
        if isinstance(new, list):
            for l in new:
                self.add_loan(l)
        elif isinstance(new, Loan):
            self.Q.append(new)
        else:
            raise TypeError

    # Return a PriorityQueue of branch loans from instance
    def branch(self):
        return PriorityQueue([l.branch() for l in self.Q], self.budget, title=self.title)

    # Order loans based on key (not neccessary for cascade or ice_slide)
    def prioritize(self, key='balance'):
        if key == 'avalanche':
            # Sort by IR
            self.Q.sort(key=lambda loan: (loan.int_rate, loan.current_bal))
            return self
        elif key == 'blizzard':
            # Sorty by monthly interest cost
            self.Q.sort(key=lambda loan: (loan.get_int_due()))
            return self
        elif key == 'snowball':
            # Sort by descending balance
            self.Q.sort(key=lambda loan: (loan.current_bal), reverse=True)
            return self
        elif key == 'balance':
            # Sort by descending balance
            self.Q.sort(key=lambda loan: (loan.start_balance), reverse=True)
            return self

    # Set payment amounts in each loan based on key
    # Return remainder of budget after min satisfied
    def set_all_payments(self, key):
        b = self.budget
        for loan in self.Q:
            if key == 'int':
                loan.payment_amt = loan.get_int_due()
            elif key == 'min':
                loan.payment_amt = loan.min_payment
            elif key == 'avg':
                loan.payment_amt = (self.budget / self.size)
            b -= loan.payment_amt

        # Handle payments not covering minimum by raising error for now
        if b < 0:
            print("Budget cannot cover loan payments.")
            raise ValueError
        return b

    def distribute(self, key, r):
        # Spread-style distribution
        if key == 'cascade' or key == 'ice_slide':
            self.spread(key, r)
        # Target-style distribution
        else:
            self.Q[-1].payment_amt += r

    def spread(self, key, r):
        # Cascade spreads remainder proportional to impact on total IR
        if key == 'cascade':
            total = sum([l.int_rate for l in self.Q])
            extra = [((l.int_rate / total) * r) for l in self.Q]

        # Ice Slide spreads remainder proportional to impact on total MI
        elif key == 'ice_slide':
            total = sum([l.get_int_due() for l in self.Q])
            extra = [((l.get_int_due() / total) * r) for l in self.Q]

        # Distribute
        for i in range(self.size):
                self.Q[i].payment_amt += extra[i]

    ############################################################
    #   ALGORITHM METHODS
    ############################################################
    # ORDERED:      Focus on targeting a single loan each cycle,
    #               paying only minimums on all except target,
    #               paying one off at a time
    ############################################################
    # Avalanche:    Order loans by interest rate, balance,
    #               target highest ir until all paid off.
    #               Consistently results in lowest interest paid
    #               over course of large loans.
    def avalanche(self, minimum='int'):
        return self.debt_solve('avalanche', minimum)
    ############################################################
    # Blizzard:     Order loans by monthly interest cost,
    #               target most expensive until all paid off.
    #               Provides some benefits for small loans,
    #               and/or large budgets
    def blizzard(self, minimum='int'):
        return self.debt_solve('blizzard', minimum)
    ############################################################
    # Snowball:     Order loans by balance, target loan with
    #               lowest starting bal, pay until all paid off.
    #               Largely motivaitonal, not cost-effective.
    def snowball(self, minimum='int'):
        return self.debt_solve('snowball', minimum)
    ############################################################
    # UNORDERED:    Focus on spreading payments strategically, rather
    #               than strict targeting. In the short term, these
    #               methods can reduce monthly cost.
    ############################################################
    # Cascade:      Unordered, distribute % of budget to each loan
    #               proportional to its % contribution to total
    #               interest rate of all loans.
    def cascade(self, minimum='int'):
        return self.debt_solve('cascade', minimum)
    ############################################################
    # Ice Slide:    Unordered, distribute % of budget to each loan
    #               proportional to its % contribution to total
    #               monthly cost (minimum payments) of all loans.
    def ice_slide(self, minimum='int'):
        return self.debt_solve('ice_slide', minimum)
    ############################################################

    # Do all methods, return MethodCompare obj of Queues sorted by "best"
    def finish(self, goal='interest', minimum='int'):
        all_complete = MethodCompare([
            self.avalanche(minimum),
            self.cascade(minimum),
            self.blizzard(minimum),
            self.ice_slide(minimum),
            self.snowball(minimum)
         ])
        all_complete.order_by(goal)
        return all_complete

    # Main algo driver, solve-in-place, returns completed PriorityQueue
    def debt_solve(self, key, minimum):
        # Method logic map
        order_once = (key == "avalanche" or key == "snowball")
        order_every = (key == "blizzard")

        # 1) Create tempQ(branch), completedQ(empty) structures
        temp_queue = self.branch()
        completed_queue = PriorityQueue([], self.budget, title=self.title)

        # Initial ordering
        if order_once:
            temp_queue.prioritize(key)

        # 4) Execute method until all loans popped from temp->completed
        while temp_queue.size > 0:
            # 3) Step through payments until at least one reaches 0
            while all([not l.is_complete() for l in temp_queue.Q]):

                if order_every:
                    temp_queue.prioritize(key)

                # Set minimums, remainder is budget leftover (raises error if<0)
                remainder = temp_queue.set_all_payments(minimum)

                # Distribute remainder
                temp_queue.distribute(key, remainder)

                # Make one payment for each loan in temp
                for loan in temp_queue.Q:
                    loan.pay_month()

            # "Pop" paidoff loan(s) to completed queue
            paid_off = [l for l in temp_queue.Q if l.is_complete()]
            for l in paid_off:
                completed_queue.add_loan(l)
                temp_queue.Q.remove(l)

        # After every Loan completes, reorder and return completed Queue
        return completed_queue.prioritize()
    
    # Solve-in-place every loan in the queue
    def payoff(self):
        # self.set_all_payments(minimum)
        all_valid = True
        for loan in self.Q:
            if not loan.payoff().is_complete(): all_valid = False
        return all_valid
        

    ######################
    #   DISPLAY METHODS
    ######################
    @staticmethod
    def line():
        print('-' * 30)
    
    def display_info(self, expand=False, histories=False):
        self.line()
        print(f'Queue title: {self.title}')
        # If we're displaying a completed loan, show completed info
        if self.is_complete():
            print(f'Loan order: {self.Q}')
            print(f'Duration: {self.get_duration()}')
            print(f'Total number of payments: {self.get_num_payments()}')
            print(f'Total interest paid: {self.get_interest_paid()}')
            print(f'Percent towards principal: {self.get_percent_principal()}')
        # If we're displaying an incomplete loan, display initial conditions
        else:
            print(f'Budget: {self.budget}')
            for l in self.Q:
                print(f'{l}: {l.start_balance}, {l.int_rate}')
        self.line()
        if expand:
            self.expanded_info()
        if histories:
            self.history_info()

    # Display individual loan info
    def expanded_info(self):
        self.line()
        for l in self.Q:
            for i in l.get_payment_info():
                print(i)
            self.line()

    # Display individual loan histories
    def history_info(self):
        self.line()
        print(f'{self.title} Payment History')
        for l in self.Q:
            self.line()
            print(f'{l.title} history:')
            for k, v in l.Payment_History.items():
                 print(k, [str(p) for p in v])
            self.line()
