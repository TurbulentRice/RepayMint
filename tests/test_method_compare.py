import unittest
import random
from app.loan import StandardLoan
from app.priority_queue import PriorityQueue
from app.method_compare import MethodCompare

class PriorityQueueTest(unittest.TestCase):
  def setUp(self):
    
    self.budget = 750
    self.loans = [
      StandardLoan(3245.65, 4.41, title="2014", term=36),
      StandardLoan(12002.91, 3.61, title="2013", term=120),
      StandardLoan(2481.30, 6.1, title="2012", term=60),
      StandardLoan(5930.42, 6.1, title="2011", term=120)
    ]

    # Start our primary queue and display
    self.priority_queue = PriorityQueue(self.loans, self.budget, title="Test Loans")
    # Get a MethodCompare obj
    minimum = 'int'
    self.avalanche, self.cascade, self.blizzard, self.ice_slide, self.snowball = [
      self.priority_queue.avalanche(minimum),
      self.priority_queue.cascade(minimum),
      self.priority_queue.blizzard(minimum),
      self.priority_queue.ice_slide(minimum),
      self.priority_queue.snowball(minimum)
    ]
    self.method_compare = MethodCompare([self.avalanche, self.cascade, self.blizzard, self.ice_slide, self.snowball])

  def test_order_by_interest(self):
    self.method_compare.order_by('interest')
    self.assertLessEqual(self.method_compare.grid[0].get_interest_paid(), self.method_compare.grid[1].get_interest_paid())
    self.assertLessEqual(self.method_compare.grid[1].get_interest_paid(), self.method_compare.grid[2].get_interest_paid())
    self.assertLessEqual(self.method_compare.grid[2].get_interest_paid(), self.method_compare.grid[3].get_interest_paid())
    self.assertLessEqual(self.method_compare.grid[3].get_interest_paid(), self.method_compare.grid[4].get_interest_paid())

  def test_order_by_time(self):
    self.method_compare.order_by('time')
    self.assertLessEqual(self.method_compare.grid[0].get_duration(), self.method_compare.grid[1].get_duration())
    self.assertLessEqual(self.method_compare.grid[1].get_duration(), self.method_compare.grid[2].get_duration())
    self.assertLessEqual(self.method_compare.grid[2].get_duration(), self.method_compare.grid[3].get_duration())
    self.assertLessEqual(self.method_compare.grid[3].get_duration(), self.method_compare.grid[4].get_duration())

  def test_order_by_fewest_payments(self):
    self.method_compare.order_by('num_p')
    self.assertLessEqual(self.method_compare.grid[0].get_num_payments(), self.method_compare.grid[1].get_num_payments())
    self.assertLessEqual(self.method_compare.grid[1].get_num_payments(), self.method_compare.grid[2].get_num_payments())
    self.assertLessEqual(self.method_compare.grid[2].get_num_payments(), self.method_compare.grid[3].get_num_payments())
    self.assertLessEqual(self.method_compare.grid[3].get_num_payments(), self.method_compare.grid[4].get_num_payments())

if __name__ == "main":
  unittest.main()
