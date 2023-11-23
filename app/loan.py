#   Loan data structures
#   Models loan amortization schedules
#   Pay, pay months, and payoff commands (step, steps, complete)
#   Performs replicative modeling for comparing with other Loans

from decimal import *

#########################################
#   BASE CLASS
#########################################

class Loan:
    #   Class counters
    #   We'll use these to keep track of instances during runtime
    INSTANCE_COUNTER = 0
    UNTITLED_COUNTER = 0

    def __init__(self, sb, ir, pa=0, title=None, term=None):
        #   Count this instance
        Loan.INSTANCE_COUNTER += 1

        #   Primary attributes
        self.title = title
        self.term = term
        self.start_balance = sb
        self.int_rate = ir
        self.payment_amt = pa

        #   Payment History {Dict of [Lists]}
        #   Main ledger object for reading/writing transactions
        self.Payment_History = {
            "balance": [self.start_balance],
            "principal": [self.Dec(0)],
            "interest": [self.Dec(0)],
            "pay_no": [0]
        }

    ###############################
    #   PRIMARY GETTER / SETTERS
    ###############################
    #   Encapsulates primary instance attributes
    #   Enhances attribute setting by ensuring proper type/format
    #   Since we are working with Decimals, type/format is crucial

    #   Title
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, t):
        if not t:
            Loan.UNTITLED_COUNTER += 1
            self._title = f"Untitled({Loan.UNTITLED_COUNTER})"
        else:
            self._title = t

    #   Term
    @property
    def term(self):
        return self._term
    @term.setter
    def term(self, m):
        if not m:
            self._term = 12
        else:
            self._term = int(m)

    #   Start balance
    @property
    def start_balance(self):
        return self._start_balance
    @start_balance.setter
    def start_balance(self, n):
        self._start_balance = self.Dec(n)

    #   Interest rate
    @property
    def int_rate(self):
        return self._int_rate
    @int_rate.setter
    def int_rate(self, n):
        self._int_rate = self.Dec(n)

    #   Payment amount
    @property
    def payment_amt(self):
        return self._payment_amt
    @payment_amt.setter
    def payment_amt(self, n):
        self._payment_amt = self.Dec(n)

    def to_json(self):
        return {
            "title": self.title,
            "term": self.term,
            "start_balance": self.start_balance,
            "int_rate": self.int_rate,
            "payment_amt": self.payment_amt,
            "payment_history": self.Payment_History
        }

    #######################
    #   GENERAL METHODS
    #######################
     #   Object str/repr
    def __str__(self):
        return self.title
    def __repr__(self):
        return self.title

    #   Static rounding function
    #   Takes number obj, convert to Decimal if necessary, round to 2 places
    @staticmethod
    def Dec(n):
        cent = Decimal('0.01')
        if not isinstance(n, Decimal):
            n = Decimal(str(n))
        return n.quantize(cent, ROUND_HALF_UP)

    #   Check if loan is paid off
    def is_complete(self):
        return (self.current_bal == 0)

    def get_payment_info(self):
        return [
            f"Title: {self.title}",
            f"Starting Balance: {self.start_balance}",
            f"Current Balance: ${self.current_bal}",
            f"Interest Rate: {self.int_rate}%",
            f"Number of payments made: {self.pay_no}",
            f"Interest Paid: ${self.get_interest_paid()}, {self.get_p_to_i('i')}%",
            f"Principal Paid: ${self.get_principal_paid()}, {self.get_p_to_i('p')}%",
            f"Total Paid: ${self.get_total_paid()}",
            f"Principal to Interest Ratio: {self.get_p_to_i()}:1"
        ]

    #######################################
    #   COMPUTATION ATTRIBUTES / METHODS
    #######################################

    #   Properties perform pertinent, heavily used retrievals

    # Determine minimum payment amount (unquantized)
    @property
    def min_payment(self):
        # Discount factor = {[(1+r)n]-1}/[r(1+r)^n]
        def discount_factor():
            r = self.get_monthly_ir()
            n = self.term
            return (((1 + r) ** n) - 1) / (r * (1 + r) ** n)
        return self.start_balance / discount_factor()


    @property
    def current_bal(self):
        return self.Payment_History['balance'][-1]

    @property
    def pay_no(self):
        return self.Payment_History['pay_no'][-1]

    #   Methods perform calculations

    def get_monthly_ir(self):
        return (self.int_rate / 12) / 100

    def get_int_due(self):
        return self.get_monthly_ir() * self.current_bal

    def get_interest_paid(self):
        return sum(self.Payment_History['interest'])

    def get_principal_paid(self):
        return sum(self.Payment_History['principal'])

    def get_total_paid(self):
        return self.get_interest_paid() + self.get_principal_paid()

    def get_p_to_i(self, c=None):
        if not self.get_total_paid():
            return 0
        if c is None:
            return self.Dec(self.get_principal_paid() / self.get_interest_paid())
        elif c == 'p':
            return self.Dec(self.get_principal_paid() / self.get_total_paid() * 100)
        elif c == 'i':
            return self.Dec(self.get_interest_paid() / self.get_total_paid() * 100)

    ###########################
    #   PAYMENT METHODS
    ###########################
    #   Records a new entry in Payment_History
    def install_payment(self, b, p, i):
        self.Payment_History['balance'].append(self.Dec(b))
        self.Payment_History['principal'].append(self.Dec(p))
        self.Payment_History['interest'].append(self.Dec(i))
        self.Payment_History['pay_no'].append(self.pay_no + 1)

    #   Make one Payment
    def pay_month(self):
        #   Calculate interest due and subtract from principal payment
        int_payment = self.get_int_due()
        principal_payment = self.payment_amt - int_payment

        #   If principal_payment is greater than balance,
        if principal_payment > self.current_bal:
            #   only pay current balance (never overpay)
            principal_payment = self.current_bal

        #   Calculate balance forward (capitalize or reduce)
        bal_fwd = self.current_bal - principal_payment

        #   If payment won't cover interest (negative principal_payment),
        if principal_payment < 0:
            #   entire payment goes to interest, no principal payment
            int_payment = self.payment_amt
            principal_payment = 0

        #   Install payment
        self.install_payment(bal_fwd, principal_payment, int_payment)

    #   Make m payments, checking for completion each iteration
    def pay_months(self, m: int):
        for i in range(m):
            if self.is_complete():
                break
            self.pay_month()

    #   Make payments until repayment complete, return T or F based on completion
    def payoff(self):
        #   Handle infinite loop (payments can't cover interest)
        if self.payment_amt <= self.get_int_due():
            return False

        #   Otherwise, loop until paid off
        while not self.is_complete():
            self.pay_month()

        print(f'payoff() call on "{self.title}" made {self.pay_no} calculations')
        return True

#########################################
#   CHILD CLASS
#########################################

#   Inherits all from parent, added duplicative pay methods
class StandardLoan(Loan):

    ###############################################
    #   ITERATIVE DUPLICATIVE SOLVE METHODS
    ###############################################

    # Return a new StandardLoan using self's state as init data
    def branch(self, t=None):
        b = self.current_bal
        i = self.int_rate
        pa = self.payment_amt
        t = self.title if t is None else f"{self.title} {t}"
        m = self.term
        return StandardLoan(b, i, pa, title=t, term=m)

    # Call payoff() on a branch of self
    # Return paid branch loan obj
    def solve(self):
        branch = self.branch()
        if branch.payoff():
            return branch
        
        print("Did not complete repayment")

    ###############################################
    #   RECURSIVE DUPLICATIVE SOLVE METHODS
    ###############################################
    # BENEFITS:
    # Marginal time benefit with small # of calculations
    # TIME TRIAL:
    # iterations        154         516         992(max recursive depth)
    # solve_in_place(): 0.00040s    0.0012s     0.0024
    # payoff():         0.00035s    0.0011s     0.0023
    # rec_solve():      0.00019s    0.0013s     0.0019
    # DISADVANTAGES OF RECURSION:
    # Depth = nump_p, maximum ~= 1000 iterations,

    # Wrappers for solve()
    def solve_for_interest(self):
        return self.recursive_solve()[1]
    def solve_for_np(self):
        return self.recursive_solve()[2]

    #   Recursive Pay Method
    #   Models an amortization schedule w/o altering object
    #   goal = number of payments to make
    def recursive_solve(self, goal=None):
        #   Inner function performs recursive pay
        def inner(c_bal, i_c=0, num_p=0):
            #   End condition: Balance reaches 0, or num payments satisfied
            if c_bal == 0 or num_p == goal:
                print(f'This solve() call on {self.title} made {num_p} calculations')
                # Also, should we consider any amount paid over s_bal to be int?
                # All extra is, after all, just capitalized int
                # so i_c += (principal_paid - s_bal)
                return [c_bal, i_c, num_p]
            #   Body of loop, mirrors implementation of Loan.pay_month()
            ip = _mir * c_bal
            pmt = _pa - ip
            #   Handle underpayment/overpayment
            if pmt < 0:
                ip = _pa
            elif pmt >= c_bal:
                pmt = c_bal

            return inner(c_bal-pmt, i_c+ip, num_p+1)

        #   Outer layer captures current loan state for use by inner
        s_bal = self.current_bal
        _mir = self.get_monthly_ir()
        _pa = self.payment_amt

        #   Don't execute if no goal is set and payments can't cover interest
        if (goal is None) and (_pa <= (_mir * s_bal)):
            print("Minimum payment not met")
            return [s_bal, 0, 0]

        #   Otherwise, call recursive inner,
        return inner(s_bal)
